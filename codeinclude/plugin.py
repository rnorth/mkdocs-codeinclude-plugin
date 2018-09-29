from mkdocs.plugins import BasePlugin
import re
import os



class CodeIncludePlugin(BasePlugin):
    def on_page_markdown(self, markdown, page, config,
                          site_navigation=None, **kwargs):
        "Provide a hook for defining functions from an external module"
        print(page.file.abs_src_path)

        def repl(m):
            filename = m.group(1)

            page_parent_dir = os.path.dirname(page.file.abs_src_path)
            import_path = os.path.join(page_parent_dir, filename)

            with open(import_path) as f:
                content = f.read()

            return "<pre><code>" + content + "</code></pre>"

        return re.sub(r'% codeinclude ([^\s]+) %', repl, markdown)
