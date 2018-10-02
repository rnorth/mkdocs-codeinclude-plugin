import re


def select(text, 
           lines=None, 
           from_token=None, to_token=None, 
           block=None, 
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
            print(delim_count)
            if block in line and delim_count <= 0:
                print("starting")
                delim_count = 0
                delim_count += line.count("{")
                
            if delim_count > 0:
                print(line)
                selected_lines.append(i)

            delim_count -= line.count("}")

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
        if i > (last_selected + 1):
            result += "\n⋯\n\n"
        result += source_lines[i - 1] + "\n"
        last_selected = i

    return result


s = """
a
b
c
d
e
f
g
h
i
j
k
l
"""

print(select(s, lines="3-7,1"))