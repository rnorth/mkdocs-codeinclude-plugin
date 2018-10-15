import re


def select(text, 
           lines=None, 
           from_token=None, to_token=None, 
           block=None,
           inside_block=None, 
           lang=None):
    
    selected_lines = []

    if lines:
        for line_range in lines.split(","):
            range_match = re.match(r'(\d+)-(\d+)', line_range)
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
            i = i + 1
            if block in line and delim_count <= 0:
                delim_count = 0

            delim_count += line.count("{")
                
            if delim_count > 0:
                selected_lines.append(i)

            delim_count -= line.count("}")

    if inside_block:
        i = 0
        delim_count = 0
        for line in text.splitlines():
            first_line_of_block = False
            i = i + 1
            if inside_block in line and delim_count <= 0:
                delim_count = 0
                first_line_of_block = True
            
            delim_count += line.count("{")
            delim_count -= line.count("}")
                
            if delim_count > 0 and not first_line_of_block:
                selected_lines.append(i)

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
            result += "\n⋯\n\n"
        result += source_lines[i - 1] + "\n"
        last_selected = i

    return result
