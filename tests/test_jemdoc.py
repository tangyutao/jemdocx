import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
JEMDOC = ROOT / "jemdoc.py"
COMPAT_ENTRY = ROOT / "jemdoc"
DOCS = ROOT / "docs"


class JemdocTests(unittest.TestCase):
    def run_jemdoc(self, *arguments, cwd=None):
        return subprocess.run(
            [sys.executable, str(JEMDOC), *map(str, arguments)],
            cwd=cwd,
            check=True,
            capture_output=True,
            text=True,
            encoding="utf-8",
        )

    def test_help(self):
        result = self.run_jemdoc("--help")
        self.assertIn("usage: jemdoc.py", result.stdout)
        self.assertIn("--math {mathjax,png,none}", result.stdout)

    def test_version(self):
        result = self.run_jemdoc("--version")
        self.assertIn("jemdocx 1.0.0", result.stdout)

    def test_extension_may_be_omitted_and_options_may_follow_source(self):
        with tempfile.TemporaryDirectory() as directory:
            workdir = Path(directory)
            output_dir = workdir / "output"
            output_dir.mkdir()
            (workdir / "input.jemdoc").write_text(
                "# jemdoc: nofooter\n= Direct invocation\n\nValue $x$.\n",
                encoding="utf-8",
            )

            self.run_jemdoc(
                "input",
                "--math",
                "none",
                "-o",
                output_dir,
                cwd=workdir,
            )

            output = (output_dir / "input.html").read_text(encoding="utf-8")
            self.assertIn("<title>Direct invocation</title>", output)
            self.assertIn("Value $x$.", output)

    def test_extensionless_compatibility_entry_point(self):
        result = subprocess.run(
            [sys.executable, str(COMPAT_ENTRY), "--version"],
            check=True,
            capture_output=True,
            text=True,
            encoding="utf-8",
        )
        self.assertIn("jemdocx 1.0.0", result.stdout)

    def test_generates_utf8_html_with_menu_and_include(self):
        with tempfile.TemporaryDirectory() as directory:
            workdir = Path(directory)
            (workdir / "MENU").write_text(
                "Pages\nHome [index.html]\nResearch\nPublications [publications.html]\n",
                encoding="utf-8",
            )
            (workdir / "included.txt").write_text(
                "<span>原始 HTML</span>\n", encoding="utf-8"
            )
            source = workdir / "index.jemdoc"
            source.write_text(
                "# jemdoc: menu{MENU}{index.html}, nofooter\n"
                "= 现代化的 jemdoc\n"
                "欢迎使用 *Python 3*。\n"
                "#includeraw{included.txt}\n",
                encoding="utf-8",
            )

            self.run_jemdoc(source.name, cwd=workdir)

            output = (workdir / "index.html").read_text(encoding="utf-8")
            self.assertIn("<title>现代化的 jemdoc</title>", output)
            self.assertIn("欢迎使用 <b>Python 3</b>。", output)
            self.assertIn('<a href="index.html" class="current">Home</a>', output)
            self.assertEqual(output.count('<div class="menu-group">'), 2)
            self.assertEqual(output.count('<div class="menu-links">'), 2)
            self.assertIn(
                '<div class="menu-category">Pages</div>\n'
                '<div class="menu-links">\n'
                '<div class="menu-item"><a href="index.html" class="current">Home</a></div>',
                output,
            )
            self.assertIn(
                '<div class="menu-category">Research</div>\n'
                '<div class="menu-links">\n'
                '<div class="menu-item"><a href="publications.html">Publications</a></div>',
                output,
            )
            self.assertIn("<span>原始 HTML</span>", output)
            self.assertNotIn('id="footer"', output)

    def test_mathjax_is_the_default_equation_backend(self):
        with tempfile.TemporaryDirectory() as directory:
            workdir = Path(directory)
            source = workdir / "math.jemdoc"
            source.write_text(
                "# jemdoc: nofooter\n"
                "= Equations\n"
                "Inline $x^2 + y^2$ equation.\n"
                "\\(\n"
                "\\frac{-b \\pm \\sqrt{b^2-4ac}}{2a}\n"
                "\\)\n",
                encoding="utf-8",
            )

            self.run_jemdoc(source.name, cwd=workdir)

            output = (workdir / "math.html").read_text(encoding="utf-8")
            self.assertIn("mathjax@4/tex-mml-chtml.js", output)
            self.assertIn(r"\(x^2 + y^2\)", output)
            self.assertIn(r"\[\frac{-b \pm \sqrt{b^2-4ac}}{2a}\]", output)
            self.assertNotIn("<img class=\"eq\"", output)

    def test_math_none_leaves_equations_unprocessed(self):
        with tempfile.TemporaryDirectory() as directory:
            workdir = Path(directory)
            source = workdir / "math.jemdoc"
            source.write_text("= No math\nValue $x$.\n", encoding="utf-8")

            self.run_jemdoc("--math", "none", source.name, cwd=workdir)

            output = (workdir / "math.html").read_text(encoding="utf-8")
            self.assertNotIn("mathjax@4", output)
            self.assertIn("Value $x$.", output)
            self.assertIn(
                '<a href="https://github.com/tangyutao/jemdocx">jemdocx</a>',
                output,
            )

    def test_analytics_uses_the_current_google_tag(self):
        with tempfile.TemporaryDirectory() as directory:
            workdir = Path(directory)
            source = workdir / "analytics.jemdoc"
            source.write_text(
                "# jemdoc: analytics{G-TEST123}, nofooter\n= Analytics\n",
                encoding="utf-8",
            )

            self.run_jemdoc(source.name, cwd=workdir)

            output = (workdir / "analytics.html").read_text(encoding="utf-8")
            self.assertIn(
                "https://www.googletagmanager.com/gtag/js?id=G-TEST123",
                output,
            )
            self.assertIn("gtag('config', 'G-TEST123')", output)
            self.assertNotIn("google-analytics.com/ga.js", output)

    def test_all_documentation_pages_build(self):
        sources = sorted(DOCS.glob("*.jemdoc"))
        self.assertTrue(sources)

        with tempfile.TemporaryDirectory() as directory:
            output_dir = Path(directory)
            for source in sources:
                self.run_jemdoc(
                    "-o",
                    output_dir / f"{source.stem}.html",
                    "-c",
                    "jemdoc.conf",
                    source.name,
                    cwd=DOCS,
                )

            self.assertEqual(
                len(sources),
                len(list(output_dir.glob("*.html"))),
            )


if __name__ == "__main__":
    unittest.main()
