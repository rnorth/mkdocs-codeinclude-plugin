from mkdocs.plugins import BasePlugin
import re
import os

from codeinclude.resolver import select

RE_SNIPPET = r'''(?x)
    \[(?P<filename>[^\]]+)\]
    \(
    snippet[ \t]*
    (lang=(?P<lang>[a-z0-9]+))?[ \t]*
    (lines=(?P<lines>[0-9,\-]+))?[ \t]*
    (from_token=(?P<from_token>[^\s]+))?[ \t]*
    (to_token=(?P<to_token>[^\s]+))?[ \t]*
    (block=(?P<block>[^\s]+))?[ \t]*
    \)
'''

class CodeIncludePlugin(BasePlugin):
    def on_page_markdown(self, markdown, page, config,
                         site_navigation=None, **kwargs):
        "Provide a hook for defining functions from an external module"
        print(page.file.abs_src_path)

        def repl(m):
            print(m)
            filename = m.group("filename")
            lang = m.group("lang") or ""
            lines = m.group("lines")
            from_token = m.group("from_token")
            to_token = m.group("to_token")
            block = m.group("block")

            page_parent_dir = os.path.dirname(page.file.abs_src_path)
            import_path = os.path.join(page_parent_dir, filename)
            print(filename)
            print(import_path)
            with open(import_path) as f:
                content = f.read()

            selected_content = select(content, lines=lines, block=block, from_token=from_token, to_token=to_token)

            return str.format("\n\n```{}\n{}\n```\n\n", lang, selected_content)

        return re.sub(RE_SNIPPET, repl, markdown)
