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

    def test_block_curly_on_same_line(self):
        result = select(
            textwrap.dedent(
                """
                /* Before foo */
                foo {
                  /* {} {@code Bar} */
                }
                /* After foo */
                """),
            block="foo")
        self.assertEquals(("foo {\n"
                           "  /* {} {@code Bar} */\n"
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

    def test_inside_block_in_a_block(self):
        result = select(
            textwrap.dedent(
                """
                {{{
                foo {
                  /* inside foo */
                }
                }}}
                """),
            inside_block="foo")
        self.assertEquals("  /* inside foo */\n", result)

    def test_inside_block_contains_keyword(self):
        result = select(
            textwrap.dedent(
                """
                  /* Some code before {} */
                  first {
                    /* first */
                    first();
                    if (first()) {
                      first();
                    } else {
                      first();
                    }
                  }
                  /* Some code after {} */
                """),
            inside_block="first")
        self.maxDiff = None
        self.assertEquals(
"""  /* first */
  first();
  if (first()) {
    first();
  } else {
    first();
  }
""",
            result)

    def test_inside_block_nested_matching_blocks(self):
        result = select(
            textwrap.dedent(
                """
                  /* Some code before {} */
                  first {
                    first {
                      first {
                        /* The most deeply nested. */
                      } 
                    }
                  }
                  /* Some code after {} */
                """),
            inside_block="first")
        self.maxDiff = None
        self.assertEquals(
"""  first {
    first {
      /* The most deeply nested. */
    } 
  }
""",
            result)

    def test_inside_block_multiple_blocks_first(self):
        result = select(
            textwrap.dedent(
                """
                  /* Some code before {} */
                  first {
                    /* inside first */
                  }
                  /* Some code in between */
                  second {
                    /* inside second */
                  }
                  /* Some code after {} */
                """),
            inside_block="first")
        self.maxDiff = None
        self.assertEquals("  /* inside first */\n", result)

    def test_inside_block_multiple_blocks_second(self):
        result = select(
            textwrap.dedent(
                """
                  /* Some code before {} */
                  first {
                    /* inside first */
                  }
                  /* Some code in between */
                  second {
                    /* inside second */
                  }
                  /* Some code after {} */
                """),
            inside_block="second")
        self.maxDiff = None
        self.assertEquals("  /* inside second */\n", result)

    def test_inside_block_several_matching_blocks(self):
        result = select(
            textwrap.dedent(
                """
                  /* Some code before {} */
                  matching_block 1 {
                    /* inside first */
                  }
                  /* Some code in between */
                  matching_block 2 {
                    /* inside second */
                  }
                  /* Some code after {} */
                """),
            inside_block="matching_block")
        self.maxDiff = None
        self.assertEquals(("  /* inside first */\n"
                           "\n⋯\n\n"
                           "  /* inside second */\n"),
                          result)
