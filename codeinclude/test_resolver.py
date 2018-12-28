import unittest

from codeinclude.resolver import select

CODE_BLOCK_EXAMPLE = """
this is the first line
blockstarter {
    block content
}
this is a trailing line
"""

def test_lines():
    result = select(CODE_BLOCK_EXAMPLE, lines="1,5")
    assert result == ("this is the first line\n"
                      "this is a trailing line")

def test_inside_block():
    result = select(CODE_BLOCK_EXAMPLE, inside_block="blockstarter")
    assert result == "block content"

def test_whole_block():
    result = select(CODE_BLOCK_EXAMPLE, block="blockstarter")
    assert result == ("blockstarter {\n"
                      "    block content\n"
                      "}")