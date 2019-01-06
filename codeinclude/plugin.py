import re
import os
import shlex
import textwrap

from mkdocs.plugins import BasePlugin
from codeinclude.resolver import select

RE_SNIPPET = r"""(?x)
    ^
    (?P<leading_space>\s*)
    (?P<marker><!--codeinclude-->)
    (?P<ignored_space>\s*)
    \[(?P<title>[^\]]*)\]\((?P<filename>[^)]+)\)
    ([\t ]+(?P<params>.*))?
    $
"""


def get_substitute(page, title, filename, lines, block, inside_block):

    page_parent_dir = os.path.dirname(page.file.abs_src_path)
    import_path = os.path.join(page_parent_dir, filename)
    with open(import_path) as f:
        content = f.read()

    selected_content = select(
        content, lines=lines, block=block, inside_block=inside_block
    )

    dedented = textwrap.dedent(selected_content)

    return '\n```java tab="' + title + '"\n' + dedented + "\n```\n\n"


class CodeIncludePlugin(BasePlugin):
    def on_page_markdown(self, markdown, page, config, site_navigation=None, **kwargs):
        "Provide a hook for defining functions from an external module"

        results = ""
        for line in markdown.splitlines():

            # handle each line
            snippet_match = re.match(RE_SNIPPET, line)
            if snippet_match:
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
                results += code_block
            else:
                results += line + "\n"

        return results
