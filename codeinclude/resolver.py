import re
import sys
from typing import List


def removeIndentation(blocks: List[List[str]]) -> List[List[str]]:
    min_difference = sys.maxsize
    for block in blocks:
        for line in block:
            original_size = len(line)
            stripped_size = len(line.lstrip())
            difference = original_size - stripped_size
            if (difference<min_difference):
                min_difference = difference
    for block in blocks:
        for i in range(0, len(block)):
            block[i] = block[i][min_difference:]
    return blocks

def joinBlocks(blocks: List[List[str]]) -> str:
    result = ""
    for block in blocks:
        if result != "":
            result += "⋯\n"
        for line in block:
            result += line
    return result

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
                delim_count += line.count("{")
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

    source_lines = text.splitlines()

    last_selected = 0
    blocks = []
    current_block = []
    for i in sorted(selected_lines):
        if i > (last_selected + 1) and last_selected != 0:
            blocks.append(current_block)
            current_block = []
        current_block.append(source_lines[i - 1]+"\n")
        last_selected = i
    blocks.append(current_block)
    blocks = removeIndentation(blocks)
    result = joinBlocks(blocks)

    if result == "":
        return text

    return result
