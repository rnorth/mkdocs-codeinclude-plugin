# Agent Instructions

## Project

mkdocs-codeinclude-plugin — an MkDocs plugin that includes code snippets into documentation pages.

## Setup

- Use `mise` for tool version management (see `.mise.toml`)
- `mise install` to install python and uv
- `uv sync --dev` to install the plugin and dev dependencies

## Testing

- Run tests with `uv run pytest tests/`
- Always run the full test suite before committing

## Architecture

- `codeinclude/plugin.py` — MkDocs plugin hook that finds `<!--codeinclude-->` blocks in markdown and substitutes code snippets
- `codeinclude/resolver.py` — selects lines/blocks from source files (by line numbers, block name, or inside_block)
- `codeinclude/languages.py` — maps file extensions to language identifiers via pygments
- `tests/codeinclude/` — unit tests; fixtures live in `tests/codeinclude/fixture/`

## Title modes

The plugin supports multiple code block title formats via the `title_mode` config option:

- `pymdownx.tabbed` (default) — `=== "title"` with 4-space indented content
- `legacy_pymdownx.superfences` — `` ```lang tab="title" ``
- `mkdocs-material` — `` ```lang title="title" ``
- `none` — no title

## Releases

- Versioning is handled by `setuptools-scm` (derives version from git tags)
- Publishing to PyPI is triggered automatically when a GitHub release is published
- CI runs on Python 3.11
