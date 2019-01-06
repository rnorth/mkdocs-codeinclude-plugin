import os
import textwrap
import unittest

from mkdocs.config import Config, DEFAULT_SCHEMA
from mkdocs.structure.files import File
from mkdocs.structure.pages import Page

from codeinclude.plugin import CodeIncludePlugin

MARKDOWN_EXAMPLE = """
# hello world

some text before
<!--codeinclude--> [foo](Foo.java)
and some text after

"""

c = Config(schema=DEFAULT_SCHEMA)
c["site_url"] = "http://example.org/"

PAGE_EXAMPLE = Page("", File(os.path.abspath("./fixture/text.md"), "/src", "/dest", False), c)

class PluginTextCase(unittest.TestCase):

    def test_simple_case(self):
        plugin = CodeIncludePlugin()
        result = plugin.on_page_markdown(MARKDOWN_EXAMPLE, PAGE_EXAMPLE, dict())

        print(result)
        self.assertEqual(result.strip(), textwrap.dedent("""
                                  # hello world
                                  
                                  some text before
                                  
                                  ```java tab=\"foo\"
                                  public class Foo {
                                  
                                  }
                                  ```
                                  
                                  and some text after
                                  """).strip())
