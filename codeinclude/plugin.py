import re
import os
import shlex
import textwrap
from dataclasses import dataclass
from typing import List

from mkdocs.plugins import BasePlugin
from codeinclude.resolver import select
from codeinclude.languages import get_lang_class

RE_START = r"""(?x)
    ^
    (?P<leading_space>\s*)
    <!--codeinclude-->
    (?P<ignored_trailing_space>\s*)
    $
"""

RE_END = r"""(?x)
    ^
    (?P<leading_space>\s*)
    <!--/codeinclude-->
    (?P<ignored_trailing_space>\s*)
    $
"""

RE_SNIPPET = r"""(?xm)
    ^
    (?P<leading_space>\s*)
    \[(?P<title>[^\]]*)\]\((?P<filename>[^)]+)\)
    ([\t\n ]+(?P<params>[\w:-]+))?
    (?P<ignored_trailing_space>\s*)
    $
"""


class CodeIncludePlugin(BasePlugin):
    def on_page_markdown(self, markdown, page, config, site_navigation=None, **kwargs):
        "Provide a hook for defining functions from an external module"

        blocks = find_code_include_blocks(markdown)
        substitutes = get_substitutes(blocks, page)
        return substitute(markdown, substitutes)


@dataclass
class CodeIncludeBlock(object):
    first_line_index: int
    last_line_index: int
    content: str


def find_code_include_blocks(markdown: str) -> List[CodeIncludeBlock]:
    ci_blocks = list()
    first = -1
    in_block = False
    lines = markdown.splitlines()
    for index, line in enumerate(lines):
        if re.match(RE_START, lines[index]):
            if in_block:
                raise ValueError(f"Found two consecutive code-include starts: at lines {first} and {index}")
            first = index
            in_block = True
        elif re.match(RE_END, lines[index]):
            if not in_block:
                raise ValueError(f"Found code-include end without preceding start at line {index}")
            last = index
            content = '\n'.join(lines[first:last + 1])
            ci_blocks.append(CodeIncludeBlock(first, last, content))
            in_block = False
    return ci_blocks


@dataclass
class Replacement(object):
    first_line_index: int
    last_line_index: int
    content: str


def get_substitutes(blocks: List[CodeIncludeBlock], page) -> List[Replacement]:
    replacements = list()
    for ci_block in blocks:
        replacement_content = ""
        for snippet_match in re.finditer(RE_SNIPPET, ci_block.content):
            title = snippet_match.group("title")
            filename = snippet_match.group("filename")
            indent = snippet_match.group("leading_space")
            raw_params = snippet_match.group("params")

            if raw_params:
                params = dict(token.split(":") for token in shlex.split(raw_params))
                lines = params.get("lines", "")
                block = params.get("block", "")
                inside_block = params.get("inside_block", "")
            else:
                lines = ""
                block = ""
                inside_block = ""

            code_block = get_substitute(
                page, title, filename, lines, block, inside_block
            )
            # re-indent
            code_block = re.sub("^", indent, code_block, flags=re.MULTILINE)

            replacement_content += code_block
        replacements.append(Replacement(ci_block.first_line_index, ci_block.last_line_index, replacement_content))
    return replacements


def get_substitute(page, title, filename, lines, block, inside_block):
    # Compute the fence header
    lang_code = get_lang_class(filename)
    header = lang_code
    title = title.strip()
    if len(title) > 0:
        header += f' tab="{title}"'

    # Select the code content
    page_parent_dir = os.path.dirname(page.file.abs_src_path)
    import_path = os.path.join(page_parent_dir, filename)
    # Always use UTF-8, as it is the recommended default for source file encodings.
    with open(import_path, encoding='UTF-8') as f:
        content = f.read()

    selected_content = select(
        content, lines=lines, block=block, inside_block=inside_block
    )

    dedented = textwrap.dedent(selected_content)

    return f'''
```{header}
{dedented}
```

'''


def substitute(markdown: str, substitutes: List[Replacement]) -> str:
    substitutes_by_first_line = dict()
    # Index substitutes by the first line
    for s in substitutes:
        substitutes_by_first_line[s.first_line_index] = s

    # Perform substitutions
    result = ""
    index = 0
    lines = markdown.splitlines()
    while index < len(lines):
        if index in substitutes_by_first_line.keys():
            # Replace the codeinclude fragment starting at this line
            substitute = substitutes_by_first_line[index]
            result += substitute.content
            index = substitute.last_line_index
        else:
            # Keep the input line
            result += lines[index] + "\n"
        index += 1
    return result
