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
    \s*
    \[(?P<title>[^\]]*)\]\((?P<filename>[^)]+)\)
    [\t ]+
    (?P<params>.*)
    $
'''

RE_OPTION = r'''(?x)
    (lines:[ \t]*(?P<lines>[0-9,\-]+))
    |
    (block:[ \t]*(?P<block>[^$]+))
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
        print(page.file.abs_src_path)

        active = False
        title = ""
        filename = ""
        lines = ""
        block = ""
        results = ""
        for line in markdown.splitlines():
            if active and re.match(RE_END, line):
                print("end")
                active = False

            if active:
                print("active")
                snippet_match = re.match(RE_SNIPPET, line)
                if snippet_match:
                    print("snippet match")
                    title = snippet_match.group("title")
                    filename = snippet_match.group("filename")
                    raw_params = snippet_match.group("params")
                    print(raw_params)
                    params = dict(token.split(":") for token in shlex.split(raw_params))
                    lines = params.get("lines", "")
                    block = params.get("block", "")

                    results += get_substitute(page, title, filename, lines, block)


            match = re.match(RE_START, line)
            if match:
                print("start")
                active = True

            if not active and not match:
                results += line + "\n"

        return results

        # def repl(m):
        #     filename = m.group("filename")
        #     lang = m.group("lang") or ""
        #     lines = m.group("lines")
        #     from_token = m.group("from_token")
        #     to_token = m.group("to_token")
        #     block = m.group("block")

        #     selected_content = select(content, lines=lines, block=block, from_token=from_token, to_token=to_token)

        #     return str.format("\n\n```{}\n{}\n```\n\n", lang, selected_content)

        # return re.sub(RE_SNIPPET, repl, markdown)
