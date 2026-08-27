# Contributing

Contributions that improve Python compatibility, correctness, documentation,
tests, accessibility, or maintainability are welcome. Please preserve classic
jemdoc syntax and output behavior unless a change is explicitly documented.

## Development workflow

1. Use Python 3.8 or newer.
2. Make a focused change with a regression test when behavior changes.
3. Run `python -m unittest discover -s tests -v`.
4. Ensure `git diff --check` reports no whitespace errors.

The test suite builds every source file under `docs/`, so documentation changes
do not require a separate build tool.

Generated HTML, equation images, caches, and local editor files should not be
committed. Keep runtime dependencies in the Python standard library unless a
new dependency has a clear, documented benefit.

## Licensing contributions

By submitting a contribution, you agree that it may be distributed under the
project's GNU General Public License, version 3 or later. Contributors retain
copyright in their contributions unless they explicitly state otherwise.
