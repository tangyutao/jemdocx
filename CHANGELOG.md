# Changelog

All notable changes maintained by this fork are documented here.

## Unreleased

- Replaced the `<table>`-based page layout (`#tlayout`/`#layout-menu`/
  `#layout-content`) with plain `<div>` elements styled by CSS Grid in the
  default `css/jemdoc.css`. This removes the table's implicit minimum width,
  which previously caused horizontal overflow on viewports roughly
  400–600px wide (between the mobile breakpoint and the desktop layout).

## 1.0.0 - 2026-08-27

- Ported the generator from Python 2 to Python 3.8 and newer.
- Standardized text, configuration, menu, include, and HTML I/O on UTF-8.
- Reworked subprocess and temporary-file handling for Python 3.
- Added MathJax 4 as the default equation renderer.
- Retained the original `latex` + `dvipng` renderer as `--math png`.
- Added `--math none` and per-document `math{...}` backend selection.
- Added responsive mobile design support, including grouped navigation on narrow screens.
- Fixed TeX backslashes being interpreted as regular-expression replacement
  escapes on recent Python releases.
- Added regression tests and a multi-version GitHub Actions workflow.
- Reorganized and refreshed the repository documentation.
- Documented that the modernization was developed with assistance from OpenAI
  Codex and reviewed by the project maintainer.

## Upstream history

This fork is based on jemdoc 0.7.3, released on 2012-11-27. Earlier release
history is preserved in the [upstream repository](https://github.com/jem/jemdoc).
