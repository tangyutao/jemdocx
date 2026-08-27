# jemdocx

`jemdocx` is a maintained fork of Jacob Mattingley's original
[jemdoc](https://github.com/jem/jemdoc), a lightweight text markup language for
building clean static websites. The upstream 0.7.3 release dates from 2012 and
targets Python 2. This fork preserves the compact jemdoc syntax while updating
the implementation and development workflow for current Python 3 releases.

The project is especially useful for academic homepages, course websites,
project documentation, and other sites that benefit from readable source files
and a small, dependency-free generator.

## Highlights

- Python 3.8+ support; Python 2 is not supported.
- UTF-8 input, configuration, menu, include, and output files.
- MathJax 4 equations by default, with no local TeX installation required.
- Optional legacy `latex` + `dvipng` equation rendering.
- Compatibility with classic jemdoc documents, menus, configuration files, and
  CSS themes.
- Standard-library-only Python runtime and automated multi-version tests.

## Requirements

- Python 3.8 or newer.
- A modern browser for pages using the default MathJax backend.
- Optional: `latex` and `dvipng` for the legacy PNG equation backend.

## Quick start

Clone the repository and run the compatibility entry point directly:

```console
python3 jemdoc index.jemdoc
```

The explicit Python filename is equivalent:

```console
python3 jemdoc.py index.jemdoc
```

On Windows, the Python launcher can be used instead:

```console
py -3 jemdoc index.jemdoc
```

This creates `index.html`. If the source filename has no extension, jemdoc also
tries the `.jemdoc` extension automatically:

```console
python3 jemdoc index
```

To select an output file or load a custom configuration:

```console
python3 jemdoc -o public/index.html -c site.conf index.jemdoc
```

Run `python3 jemdoc --help` for the command-line overview and
`python3 jemdoc --show-config` to inspect the default HTML configuration.

## Equations

MathJax 4 is the default renderer. Inline equations use `$...$`; classic jemdoc
display equations are enclosed by `\(` and `\)` on separate lines.

```text
Euler's identity is $e^{i\pi} + 1 = 0$.

\(
  (I + XY)^{-1} = I - X(I + YX)^{-1}Y
\)
```

Select a backend on the command line:

```console
python3 jemdoc --math mathjax index.jemdoc
python3 jemdoc --math png index.jemdoc
python3 jemdoc --math none index.jemdoc
```

A document can override the backend in its first-line options:

```text
# jemdoc: math{png}
```

The `png` backend retains the original behavior and requires `latex` and
`dvipng`. The default MathJax backend emits scalable, accessible browser-rendered
mathematics and does not create an `eqs/` directory.

## Documentation

The maintained source documentation and examples are in [`docs/`](docs/). They
are ordinary jemdoc files and are also built automatically by the test suite.
The main stylesheet and additional themes are available in [`css/`](css/).

## Development

Run the regression suite with:

```console
python3 -m unittest discover -s tests -v
```

Run strict compilation before the tests when checking compatibility with a new
Python release:

```console
python3 -W error::SyntaxWarning -m py_compile jemdoc jemdoc.py tests/test_jemdoc.py
python3 -m unittest discover -s tests -v
```

See [`CONTRIBUTING.md`](CONTRIBUTING.md) for contribution guidelines and
[`CHANGELOG.md`](CHANGELOG.md) for maintained-fork changes.

## Compatibility and project scope

The goal is conservative modernization: existing jemdoc source should continue
to render with minimal or no changes. New work focuses on Python compatibility,
Unicode handling, reliable builds, web standards, and maintainability rather
than expanding jemdoc into a general-purpose site framework.

Historical upstream release files are intentionally not duplicated in this
repository; they remain available from the
[upstream Git history](https://github.com/jem/jemdoc).

## Attribution and license

jemdoc was created by Jacob Mattingley in 2007. Equation-rendering portions of
the original implementation were based on work by Kamil Kisiel. The jemdocx
modernization is maintained by Yutao Tang. Original and subsequent copyright
notices are preserved in the source and summarized in [`NOTICE`](NOTICE).

### AI-assisted development disclosure

The jemdocx 1.0.0 modernization was developed by Yutao Tang with assistance
from [OpenAI Codex](https://developers.openai.com/codex/). Codex was used to
assist with the Python 3 migration, refactoring, test development,
documentation, and repository maintenance. All AI-assisted changes were
reviewed and tested by the project maintainer, who is responsible for the
resulting release.

The project is distributed under the GNU General Public License, version 3 or
later. See [`LICENSE`](LICENSE).
