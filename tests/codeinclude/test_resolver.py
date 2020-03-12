import textwrap
import unittest

from codeinclude.resolver import select

CODE_BLOCK_EXAMPLE = """
this is the first line
blockstarter {
    block content
}
this is a trailing line
"""


class ResolverTest(unittest.TestCase):
    def test_lines(self):
        result = select(CODE_BLOCK_EXAMPLE, lines="2,6")
        self.assertEquals(("this is the first line\n"
                           "\n"
                           "⋯\n"
                           "\n"
                           "this is a trailing line\n"),
                          result)

    def test_inside_block(self):
        result = select(CODE_BLOCK_EXAMPLE, inside_block="blockstarter")
        self.assertEquals("    block content\n", result)

    def test_whole_block(self):
        result = select(CODE_BLOCK_EXAMPLE, block="blockstarter")
        self.assertEquals(("blockstarter {\n"
                           "    block content\n"
                           "}\n"),
                          result)

    def test_inside_block_content_on_last_line(self):
        result = select(
            textwrap.dedent(
                """
                foo {
                  if (true) {
                    bar();
                  } } 
                /* The line above contains both the closing curly bracket for `if` and for `foo` */
                """),
            inside_block="foo")
        self.assertEquals(("  if (true) {\n"
                           "    bar();\n"),
                          result)

    def test_inside_block_curly_on_same_line(self):
        result = select(
            textwrap.dedent(
                """
                foo {
                  /* {} */
                }
                """),
            inside_block="foo")
        self.assertEquals("  /* {} */\n", result)

    def test_inside_block_multiple_curly_on_same_line(self):
        result = select(
            textwrap.dedent(
                """
                //
                foo {
                  /* {} {@code bar} {@link baz} */
                }
                """),
            inside_block="foo")
        self.assertEquals("  /* {} {@code bar} {@link baz} */\n", result)
