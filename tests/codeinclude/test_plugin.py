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

EMPTY_TITLE_MARKDOWN_EXAMPLE = """
# hello world

some text before
<!--codeinclude-->
[](Foo.java)
<!--/codeinclude-->
and some text after

"""

MARKDOWN_EXAMPLE_RIGHT_CURLY = """
# hello world

<!--codeinclude-->
[Curly](Curly.java) block:Curly
<!--/codeinclude-->
"""

MARKDOWN_EXAMPLE_MULTIMATCH = """
# hello world

<!--codeinclude-->
[MultiMatch](MultiMatch.java) inside_block:some_token
<!--/codeinclude-->
"""

c = Config(schema=DEFAULT_SCHEMA)
c["site_url"] = "http://example.org/"

PAGE_EXAMPLE = Page(
    "",
    File(
        os.path.abspath("./tests/codeinclude/fixture/text.md"), "/src", "/dest", False
    ),
    c,
)


class PluginTextCase(unittest.TestCase):
    def test_no_includes(self):
        plugin = CodeIncludePlugin()
        result = plugin.on_page_markdown(
            MARKDOWN_EXAMPLE_NO_INCLUDES, PAGE_EXAMPLE, dict()
        )

        self.assertEqual(MARKDOWN_EXAMPLE_NO_INCLUDES.strip(), result.strip())

    def test_simple_case_no_selector(self):
        plugin = CodeIncludePlugin()
        result = plugin.on_page_markdown(
            MARKDOWN_EXAMPLE_NO_SELECTOR, PAGE_EXAMPLE, dict()
        )

        print(result)
        self.assertEqual(
            textwrap.dedent(
                """
                                  # hello world

                                  some text before

                                  ```java tab=\"foo\"
                                  public class Foo {

                                  }
                                  ```

                                  and some text after
                                  """
            ).strip(),
            result.strip(),
        )

    @unittest.skip("https://github.com/rnorth/mkdocs-codeinclude-plugin/issues/13")
    def test_simple_case_right_curly_inside_block(self):
        plugin = CodeIncludePlugin()
        result = plugin.on_page_markdown(
            MARKDOWN_EXAMPLE_RIGHT_CURLY, PAGE_EXAMPLE, dict()
        )

        print(result)
        self.assertEqual(
            textwrap.dedent(
                r"""
                                  # hello world


                                  ```java tab="Curly"
                                  public class Curly {
                                    public static String RIGHT_CURLY_REGEX = "\\}";
                                  }

                                  ```
                                  """
            ).strip(),
            result.strip(),
        )

    def test_simple_case_selector_on_same_line(self):
        plugin = CodeIncludePlugin()
        result = plugin.on_page_markdown(
            MARKDOWN_EXAMPLE_SELECTOR_ON_SAME_LINE, PAGE_EXAMPLE, dict()
        )

        print(result)
        self.assertEqual(
            textwrap.dedent(
                """
                                  # hello world

                                  some text before

                                  ```java tab=\"foo\"
                                  public class Foo {

                                  ```

                                  and some text after
                                  """
            ).strip(),
            result.strip(),
        )

    def test_simple_case_selector_on_next_line(self):
        plugin = CodeIncludePlugin()
        result = plugin.on_page_markdown(
            MARKDOWN_EXAMPLE_SELECTOR_ON_NEXT_LINE, PAGE_EXAMPLE, dict()
        )

        print(result)
        self.assertEqual(
            textwrap.dedent(
                """
                                  # hello world

                                  some text before

                                  ```java tab=\"foo\"
                                  public class Foo {

                                  ```

                                  and some text after
                                  """
            ).strip(),
            result.strip(),
        )

    def test_multi_tab_case(self):
        plugin = CodeIncludePlugin()
        result = plugin.on_page_markdown(
            MULTI_TAB_MARKDOWN_EXAMPLE, PAGE_EXAMPLE, dict()
        )

        print(result)
        self.assertEqual(
            textwrap.dedent(
                """
                                  # hello world

                                  some text before

                                  ```java tab=\"foo\"
                                  public class Foo {

                                  }
                                  ```


                                  ```java tab=\"bar\"
                                  public class Bar {
                                    // This UTF-8 encoded file has some multi-byte characters: œ, ë
                                  }
                                  ```

                                  and some text after
                                  """
            ).strip(),
            result.strip(),
        )

    def test_empty_title_case(self):
        plugin = CodeIncludePlugin()
        result = plugin.on_page_markdown(
            EMPTY_TITLE_MARKDOWN_EXAMPLE, PAGE_EXAMPLE, dict()
        )

        print(result)
        self.assertEqual(
            textwrap.dedent(
                """
                                  # hello world

                                  some text before

                                  ```java
                                  public class Foo {

                                  }
                                  ```

                                  and some text after
                                  """
            ).strip(),
            result.strip(),
        )

    def test_ellipsis_indent(self):
        plugin = CodeIncludePlugin()
        result = plugin.on_page_markdown(
            MARKDOWN_EXAMPLE_MULTIMATCH, PAGE_EXAMPLE, dict()
        )

        print(result)
        self.assertEqual(
            textwrap.dedent(
                r"""
                                  # hello world


                                  ```java tab="MultiMatch"
                                  A
                                  a

                                  ⋯

                                  C
                                  c

                                  ```
                                  """
            ).strip(),
            result.strip(),
        )
