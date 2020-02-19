import os
import textwrap
import unittest

from mkdocs.config import Config, DEFAULT_SCHEMA
from mkdocs.structure.files import File
from mkdocs.structure.pages import Page

from codeinclude.plugin import CodeIncludePlugin

MARKDOWN_EXAMPLE_NO_INCLUDES = """
# hello world

some text before

"""

MARKDOWN_EXAMPLE_NO_SELECTOR = """
# hello world

some text before
<!--codeinclude-->
[foo](Foo.java)
<!--/codeinclude-->
and some text after

"""

MARKDOWN_EXAMPLE_SELECTOR_ON_SAME_LINE = """
# hello world

some text before
<!--codeinclude-->
[foo](Foo.java) lines:1
<!--/codeinclude-->
and some text after

"""

MARKDOWN_EXAMPLE_SELECTOR_ON_NEXT_LINE = """
# hello world

some text before
<!--codeinclude-->
[foo](Foo.java)
lines:1
<!--/codeinclude-->
and some text after

"""

MULTI_TAB_MARKDOWN_EXAMPLE = """
# hello world

some text before
<!--codeinclude--> 
[foo](Foo.java) 
[bar](Bar.java)
<!--/codeinclude-->
and some text after

"""

c = Config(schema=DEFAULT_SCHEMA)
c["site_url"] = "http://example.org/"

PAGE_EXAMPLE = Page("", File(os.path.abspath("./fixture/text.md"), "/src", "/dest", False), c)


class PluginTextCase(unittest.TestCase):

    def test_no_includes(self):
        plugin = CodeIncludePlugin()
        result = plugin.on_page_markdown(MARKDOWN_EXAMPLE_NO_INCLUDES, PAGE_EXAMPLE, dict())

        self.assertEqual(MARKDOWN_EXAMPLE_NO_INCLUDES.strip(),
                         result.strip())

    def test_simple_case_no_selector(self):
        plugin = CodeIncludePlugin()
        result = plugin.on_page_markdown(MARKDOWN_EXAMPLE_NO_SELECTOR, PAGE_EXAMPLE, dict())

        print(result)
        self.assertEqual(textwrap.dedent("""
                                  # hello world
                                  
                                  some text before
                                  
                                  ```java tab=\"foo\"
                                  public class Foo {
                                  
                                  }
                                  ```
                                  
                                  and some text after
                                  """).strip(),
                         result.strip())

    def test_simple_case_selector_on_same_line(self):
        plugin = CodeIncludePlugin()
        result = plugin.on_page_markdown(MARKDOWN_EXAMPLE_SELECTOR_ON_SAME_LINE, PAGE_EXAMPLE, dict())

        print(result)
        self.assertEqual(textwrap.dedent("""
                                  # hello world

                                  some text before

                                  ```java tab=\"foo\"
                                  public class Foo {
                                  
                                  ```

                                  and some text after
                                  """).strip(),
                         result.strip())

    def test_simple_case_selector_on_next_line(self):
        plugin = CodeIncludePlugin()
        result = plugin.on_page_markdown(MARKDOWN_EXAMPLE_SELECTOR_ON_NEXT_LINE, PAGE_EXAMPLE, dict())

        print(result)
        self.assertEqual(textwrap.dedent("""
                                  # hello world

                                  some text before

                                  ```java tab=\"foo\"
                                  public class Foo {
                                  
                                  ```

                                  and some text after
                                  """).strip(),
                         result.strip())

    def test_multi_tab_case(self):
        plugin = CodeIncludePlugin()
        result = plugin.on_page_markdown(MULTI_TAB_MARKDOWN_EXAMPLE, PAGE_EXAMPLE, dict())

        print(result)
        self.assertEqual(textwrap.dedent("""
                                  # hello world

                                  some text before

                                  ```java tab=\"foo\"
                                  public class Foo {

                                  }
                                  ```


                                  ```java tab=\"bar\"
                                  public class Bar {

                                  }
                                  ```

                                  and some text after
                                  """).strip(),
                         result.strip())
