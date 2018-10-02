from mkdocs.plugins import BasePlugin
import re
import os
import shlex

from codeinclude.resolver import select

RE_START = r'''(?x)
    ^
    (?P<leading_space>\s*)
    <!--codeinclude-->
    $
'''

RE_END = r'''(?x)
    ^
    (?P<leading_space>\s*)
    <!--/codeinclude-->
    $
'''

RE_SNIPPET = r'''(?x)
    ^
    (?P<leading_space>\s*)
    \[(?P<title>[^\]]*)\]\((?P<filename>[^)]+)\)
    [\t ]+
    (?P<params>.*)
    $
'''

def get_substitute(page, title, filename, lines, block):

    page_parent_dir = os.path.dirname(page.file.abs_src_path)
    import_path = os.path.join(page_parent_dir, filename)
    with open(import_path) as f:
        content = f.read()

    selected_content = select(content, lines=lines, block=block)

    return "\n```java tab=\"" + title + "\"\n" + selected_content + "\n```\n\n"

class CodeIncludePlugin(BasePlugin):
    def on_page_markdown(self, markdown, page, config,
                         site_navigation=None, **kwargs):
        "Provide a hook for defining functions from an external module"

        active = False
        results = ""
        for line in markdown.splitlines():
            boundary = False

            # detect end
            if active and re.match(RE_END, line):
                active = False
                boundary = True

            # handle each line of a codeinclude zone
            if active:
                snippet_match = re.match(RE_SNIPPET, line)
                if snippet_match:
                    title = snippet_match.group("title")
                    filename = snippet_match.group("filename")
                    indent = snippet_match.group("leading_space")
                    raw_params = snippet_match.group("params")
                    params = dict(token.split(":") for token in shlex.split(raw_params))
                    lines = params.get("lines", "")
                    block = params.get("block", "")

                    code_block = get_substitute(page, title, filename, lines, block)
                    # re-indent
                    code_block = re.sub("^", indent, code_block, flags=re.MULTILINE)
                    results += code_block

            # detect start
            if re.match(RE_START, line):
                active = True
                boundary = True

            # outside a codeinclude zone and ignoring the boundaries
            if not active and not boundary:
                results += line + "\n"

        return results
