from pygments.lexers import get_lexer_for_filename
from pygments.util import ClassNotFound


def get_lang_class(filename: str) -> str:
    """Returns the Pygments _language alias_ for the filename.

    Pygments is used by codehilite, a widely used extension for code highlighting:
    https://squidfunk.github.io/mkdocs-material/extensions/codehilite/

    The Pygments language aliases are expected to be compatible with highlight.js language classes,
    which are used by some MkDocs themes: https://www.mkdocs.org/user-guide/styling-your-docs/#built-in-themes
    For a table of 'Language -> Language Classes' in _highlight.js_,
    see https://github.com/highlightjs/highlight.js#supported-languages
    """
    try:
        lexer = get_lexer_for_filename(filename)
        return lexer.aliases[0]
    except ClassNotFound:
        return "none"
