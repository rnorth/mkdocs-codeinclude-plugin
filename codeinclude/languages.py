

def get_lang_class(filename: str) -> str:
    """Returns the highlight.js _language class_ for the filename.

    Most MkDocs themes use the highlight.js for syntax highlighting: https://www.mkdocs.org/user-guide/styling-your-docs/#built-in-themes

    highlight.js supports file extensions as language classes.
    For a table of 'Language -> Language Classes', see https://github.com/highlightjs/highlight.js#supported-languages
    """
    return get_extension(filename)


def get_extension(filename: str) -> str:
    return filename.split('.')[-1]
