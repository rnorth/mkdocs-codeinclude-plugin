import re


def select(
    text,
    lines=None,
    from_token=None,
    to_token=None,
    block=None,
    inside_block=None,
    lang=None,
):

    selected_lines = []

    if lines:
        for line_range in lines.split(","):
            range_match = re.match(r"(\d+)-(\d+)", line_range)
            if range_match:
                start = int(range_match.group(1))
                end = int(range_match.group(2))
                for i in range(start, end + 1):
                    selected_lines.append(i)
            elif line_range.strip() != "":
                selected_lines.append(int(line_range))

    if block:
        i = 0
        delim_count = 0
        for line in text.splitlines():
            first_line_of_block = False
            i = i + 1
            if block in line and delim_count <= 0:
                delim_count = 0
                first_line_of_block = True
                delim_count += line.count("{")

            if delim_count > 0:
                if not first_line_of_block:
                    delim_count += line.count("{")
                selected_lines.append(i)

            delim_count -= line.count("}")

    if inside_block:
        delim_count = 0
        inside_matching = False
        for line_number, line in enumerate(text.splitlines(), start=1):
            first_line_of_block = False
            # Detect the block beginning
            if inside_block in line and delim_count <= 0:
                delim_count = 0
                first_line_of_block = True
                inside_matching = True

            # Don't process lines that are outside the matching block
            if not inside_matching:
                continue

            # Count the brackets in the line
            delim_count += line.count("{")
            delim_count -= line.count("}")

            # If we closed the opening bracket (= dropped below 0), the matching block has ended
            if delim_count <= 0:
                inside_matching = False

            # Append the lines inside the matching block, skipping the first matching
            if inside_matching and not first_line_of_block:
                selected_lines.append(line_number)

    if from_token and to_token:
        i = 0
        active = False
        for line in text.splitlines():
            i = i + 1
            if not active and from_token in line:
                active = True

            if active:
                selected_lines.append(i)

            if active and to_token in line:
                active = False

    result = ""
    source_lines = text.splitlines()

    last_selected = 0
    for i in sorted(selected_lines):
        if i > (last_selected + 1) and last_selected != 0:
            # Add an ellipsis between non-adjacent lines
            last_line = source_lines[last_selected - 1]
            # Use the last line indent so that the result can be un-indented by the caller.
            indent = leading_spaces(last_line)
            result += f"\n{indent}⋯\n\n"
        result += source_lines[i - 1] + "\n"
        last_selected = i

    if result == "":
        return text

    return result


def leading_spaces(s: str) -> str:
    return " " * (len(s) - len(s.lstrip()))
