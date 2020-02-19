import re
import os
import shlex
import textwrap

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

RE_SNIPPET = r"""(?x)
    ^
    (?P<leading_space>\s*)
    \[(?P<title>[^\]]*)\]\((?P<filename>[^)]+)\)
    ([\t ]+(?P<params>.*))?
    (?P<ignored_trailing_space>\s*)
    $
"""


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


class CodeIncludePlugin(BasePlugin):
    def on_page_markdown(self, markdown, page, config, site_navigation=None, **kwargs):
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

            # detect start
            if re.match(RE_START, line):
                active = True
                boundary = True

            # outside a codeinclude zone and ignoring the boundaries
            if not active and not boundary:
                results += line + "\n"

        return results
