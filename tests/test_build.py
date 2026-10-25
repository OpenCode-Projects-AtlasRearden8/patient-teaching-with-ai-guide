"""Tests for build.py: markdown conversion and static-site assembly."""

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

import build as build_mod  # noqa: E402


def test_inline_renders_bold_italic_code_links():
    html_out = build_mod._inline("Try **this** and *that*, use `tools/readability.py`, see [the site](index.md).")
    assert "<strong>this</strong>" in html_out
    assert "<em>that</em>" in html_out
    assert "<code>tools/readability.py</code>" in html_out
    assert '<a href="index.md">the site</a>' in html_out


def test_inline_escapes_html_first():
    html_out = build_mod._inline("a <b> & c")
    assert "&lt;b&gt;" in html_out
    assert "&amp;" in html_out


def test_md_to_html_headings_lists_tables_code():
    md = (
        "# Big Title\n\n"
        "A first paragraph.\n"
        "Continuation of same paragraph.\n\n"
        "- [ ] unchecked item\n"
        "- [x] checked item\n"
        "- plain item\n\n"
        "1. first step\n"
        "2. second step\n\n"
        "| Instead of | Write |\n"
        "| --- | --- |\n"
    )
    html_out = build_mod.md_to_html(md)
    assert '<h1 id="big-title">Big Title</h1>' in html_out
    assert "<p>A first paragraph. Continuation of same paragraph.</p>" in html_out
    assert "&#9744;" in html_out and "&#9745;" in html_out
    assert "<ol>" in html_out and "<li>first step</li>" in html_out
    assert "<table>" in html_out and "<th>Instead of</th>" in html_out


def test_md_to_html_fenced_code_is_escaped():
    md = "```text\n<b>&raw</b>\n```"
    html_out = build_mod.md_to_html(md)
    assert "&lt;b&gt;&amp;raw&lt;/b&gt;" in html_out
    assert "<b>" not in html_out


def test_md_to_html_link_resolver_rewrites_md_links():
    md = "Read [chapter one](01-getting-started.md) next."
    resolver = lambda target: "01-getting-started.html" if target.endswith(".md") else None
    html_out = build_mod.md_to_html(md, link_resolver=resolver)
    assert 'href="01-getting-started.html"' in html_out


def test_extract_title_and_doc_pages_have_titles():
    for md_path in sorted((ROOT / "docs").glob("*.md")):
        title = build_mod.extract_title(md_path.read_text(encoding="utf-8"))
        assert title and title != "Untitled", md_path


def test_build_site_produces_linked_html_pages(tmp_path):
    written = build_mod.build_site(tmp_path / "site")
    site = tmp_path / "site"
    names = {p.name for p in written}
    assert "index.html" in names
    assert "styles.css" in names
    index_html = (site / "index.html").read_text(encoding="utf-8")
    for chapter in sorted((ROOT / "docs").glob("*.md")):
        expected = f"{chapter.stem}.html"
        page = site / expected
        assert page.exists(), expected
        assert f'href="{expected}"' in index_html
    assert (site / "samples" / "handout-rewritten.html").exists()
    assert (site / "templates" / "preprint-checklist.html").exists()


def test_built_pages_carry_global_disclaimer(tmp_path):
    build_mod.build_site(tmp_path / "site")
    for page in (tmp_path / "site").rglob("*.html"):
        text = page.read_text(encoding="utf-8")
        assert "never medical advice" in text.lower()
        assert "Never put patient data" in text
        assert "Asdale Dynamics, LLC" in text


def test_sample_pages_sample_marked_as_fabricated(tmp_path):
    build_mod.build_site(tmp_path / "site")
    for name in ("handout-original", "handout-rewritten", "fever-original", "fever-rewritten"):
        page = tmp_path / "site" / "samples" / f"{name}.html"
        assert "fabricated teaching example" in page.read_text(encoding="utf-8")


def test_cli_build_and_check(tmp_path):
    import subprocess

    env_example = None  # no secrets, no env dependence
    out = tmp_path / "site"
    result = subprocess.run(
        [sys.executable, str(ROOT / "build.py"), "--out", str(out)],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, result.stderr
    assert (out / "index.html").exists()

    check = subprocess.run(
        [sys.executable, str(ROOT / "build.py"), "--check", "--out", str(out)],
        capture_output=True,
        text=True,
    )
    assert check.returncode == 0, check.stderr
