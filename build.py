#!/usr/bin/env python3
"""build.py -- build the static HTML site from docs/ and samples/.

Education only. Local-first: pure standard library, no network, no
accounts, no keys, nothing leaves this machine.

Usage:
    python3 build.py                 # build site/
    python3 build.py --out DIR       # build into another folder
    python3 build.py --check         # verify site/ is fresh; no writes

Exit codes: 0 ok, 1 check failed or IO error, 2 usage error.
"""

from __future__ import annotations

import argparse
import html
import re
import shutil
import sys
import tempfile
from pathlib import Path
from typing import Callable

ROOT = Path(__file__).resolve().parent
DOCS_DIR = ROOT / "docs"
SAMPLES_DIR = ROOT / "samples"
TEMPLATES_DIR = ROOT / "templates"
DEFAULT_OUT = ROOT / "site"

HEADING_RE = re.compile(r"^(#{1,6})\s+(.*)$")
ULIST_RE = re.compile(r"^\s*[-*+]\s+(.*)$")
OLIST_RE = re.compile(r"^\s*(\d+)\.\s+(.*)$")
FENCE_RE = re.compile(r"^\s*(```|~~~)\s*([A-Za-z0-9_-]*)\s*$")
QUOTE_RE = re.compile(r"^\s*>\s?(.*)$")
TABLE_SEP_RE = re.compile(r"^\s*\|?\s*:?-{3,}:?\s*(\|\s*:?-{3,}:?\s*)*\|?\s*$")
HR_RE = re.compile(r"^\s*(?:-{3,}|\*{3,}|_{3,})\s*$")
CHECK_RE = re.compile(r"^\[([ xX])\]\s*(.*)$")
LINK_RE = re.compile(r"\[([^\]]+)\]\(([^)\s]+)\)")
CODE_RE = re.compile(r"`([^`]+)`")
BOLD_RE = re.compile(r"\*\*([^*]+)\*\*")
ITALIC_RE = re.compile(r"(?<!\*)\*([^*\n]+)\*(?!\*)")


def slugify(text: str) -> str:
    text = re.sub(r"[^a-z0-9\s-]", "", text.lower().strip())
    text = re.sub(r"[\s_]+", "-", text)
    return re.sub(r"-{2,}", "-", text).strip("-")[:60] or "section"

BANNER = (
    "Education only &mdash; this manual is never medical advice. "
    "Never put patient data into any AI tool."
)

SITE_TITLE = "Patient Teaching with AI: A Healthcare Worker's Manual"


# --------------------------------------------------------------------------
# Inline markdown -> HTML
# --------------------------------------------------------------------------

def _inline(text: str) -> str:
    """Render inline markdown (code, bold, italic, links) with HTML escaping."""
    placeholders: dict[str, str] = {}

    def stash(html_fragment: str) -> str:
        key = f"\x00{len(placeholders)}\x00"
        placeholders[key] = html_fragment
        return key

    def code_sub(m: re.Match[str]) -> str:
        return stash(f"<code>{html.escape(m.group(1), quote=False)}</code>")

    def bold_sub(m: re.Match[str]) -> str:
        return stash(f"<strong>{_inline(m.group(1))}</strong>")

    def italic_sub(m: re.Match[str]) -> str:
        return stash(f"<em>{_inline(m.group(1))}</em>")

    def link_sub(m: re.Match[str]) -> str:
        label = _inline(m.group(1))
        href = html.escape(m.group(2), quote=True)
        return stash(f'<a href="{href}">{label}</a>')

    out = html.escape(text, quote=False)
    out = CODE_RE.sub(code_sub, out)
    out = BOLD_RE.sub(bold_sub, out)
    out = ITALIC_RE.sub(italic_sub, out)
    out = LINK_RE.sub(link_sub, out)
    for key, value in placeholders.items():
        out = out.replace(key, value)
    return out


def _checkbox(item: str) -> tuple[str, str]:
    match = CHECK_RE.match(item)
    if not match:
        return "", item
    box = "&#9744; " if match.group(1).strip() == "" else "&#9745; "
    return box, match.group(2)


def _split_table_row(line: str) -> list[str]:
    line = line.strip()
    if line.startswith("|"):
        line = line[1:]
    if line.endswith("|"):
        line = line[:-1]
    return [cell.strip() for cell in line.split("|")]


# --------------------------------------------------------------------------
# Block markdown -> HTML
# --------------------------------------------------------------------------

def md_to_html(
    source: str,
    link_resolver: Callable[[str], str] | None = None,
) -> str:
    """Convert a markdown document to an HTML fragment (a list of blocks).

    Supports: ATX headings, fenced code, blockquotes, pipe tables, ordered
    and unordered lists (with checkbox syntax), horizontal rules, and
    paragraphs with inline formatting.
    """
    lines = source.splitlines()
    out: list[str] = []
    slug_counts: dict[str, int] = {}
    i = 0

    def heading(text: str, level: int) -> str:
        muted = re.sub(r"\*|^_|`", "", text)
        slug = slugify(muted)
        count = slug_counts.get(slug, 0)
        slug_counts[slug] = count + 1
        if count:
            slug = f"{slug}-{count + 1}"
        return f"<h{level} id=\"{slug}\">{_inline(text)}</h{level}>"

    while i < len(lines):
        line = lines[i]

        if not line.strip():
            i += 1
            continue

        fence = FENCE_RE.match(line)
        if fence:
            lang = fence.group(2)
            i += 1
            code: list[str] = []
            while i < len(lines) and not FENCE_RE.match(lines[i]):
                code.append(lines[i])
                i += 1
            i += 1  # skip closing fence
            cls = f' class="language-{escape(lang)}"' if lang else ""
            out.append(f"<pre><code{cls}>{escape(chr(10).join(code))}</code></pre>")
            continue

        heading_match = HEADING_RE.match(line)
        if heading_match:
            level = len(heading_match.group(1))
            out.append(heading(heading_match.group(2).strip(), level))
            i += 1
            continue

        if HR_RE.match(line):
            out.append("<hr>")
            i += 1
            continue

        quote_match = QUOTE_RE.match(line)
        if quote_match:
            body: list[str] = []
            while i < len(lines):
                q = QUOTE_RE.match(lines[i])
                if not q:
                    break
                body.append(q.group(1))
                i += 1
            out.append(f"<blockquote><p>{_inline(' '.join(body))}</p></blockquote>")
            continue

        if line.strip().startswith("|") and i + 1 < len(lines) and TABLE_SEP_RE.match(lines[i + 1]):
            header = _split_table_row(line)
            i += 2
            rows: list[list[str]] = []
            while i < len(lines) and lines[i].strip().startswith("|"):
                rows.append(_split_table_row(lines[i]))
                i += 1
            head = "".join(f"<th>{_inline(cell)}</th>" for cell in header)
            body_rows = "".join(
                "<tr>" + "".join(f"<td>{_inline(cell)}</td>" for cell in row) + "</tr>"
                for row in rows
            )
            out.append(f"<table><thead><tr>{head}</tr></thead><tbody>{body_rows}</tbody></table>")
            continue

        ul = ULIST_RE.match(line)
        ol = OLIST_RE.match(line)
        if ul or ol:
            ordered = bool(ol)
            tag_open, tag_close = ("<ol>", "</ol>") if ordered else ("<ul>", "</ul>")
            items: list[str] = []
            while i < len(lines):
                m = OLIST_RE.match(lines[i]) if ordered else ULIST_RE.match(lines[i])
                if not m:
                    if lines[i].startswith(("  ", "\t")) and lines[i].strip() and items:
                        items[-1] += " " + lines[i].strip()
                        i += 1
                        continue
                    break
                content = m.group(2) if ordered else m.group(1)
                box, content = _checkbox(content)
                items.append(f"<li>{box}{_inline(content)}</li>")
                i += 1
            out.append(tag_open + "".join(items) + tag_close)
            continue

        paragraph: list[str] = []
        while i < len(lines) and lines[i].strip():
            nxt = lines[i]
            if (
                FENCE_RE.match(nxt)
                or HEADING_RE.match(nxt)
                or HR_RE.match(nxt)
                or QUOTE_RE.match(nxt)
                or ULIST_RE.match(nxt)
                or OLIST_RE.match(nxt)
                or nxt.strip().startswith("|")
            ):
                break
            paragraph.append(nxt.strip())
            i += 1
        if paragraph:
            out.append(f"<p>{_inline(' '.join(paragraph))}</p>")
        else:
            i += 1  # unmatched rare case; avoid infinite loop

    html_out = "\n".join(out)
    if link_resolver is not None:
        def fix(m: re.Match[str]) -> str:
            target = html.unescape(m.group(1))
            resolved = link_resolver(target)
            if resolved is None:
                return m.group(0)
            return f'<a href="{escape(resolved)}">{m.group(2)}</a>'
        html_out = re.sub(r'<a href="([^"]+)">((?:(?!</a>).)*)</a>', fix, html_out, flags=re.S)
    return html_out


def extract_title(source: str) -> str:
    for line in source.splitlines():
        m = HEADING_RE.match(line)
        if m and len(m.group(1)) == 1:
            return re.sub(r"\*\*|^_|`", "", m.group(2)).strip()
    return "Untitled"


# --------------------------------------------------------------------------
# Site assembly
# --------------------------------------------------------------------------

STYLESHEET = """
:root { --ink:#1c2430; --paper:#fbfaf7; --accent:#0e6e5c; --warn:#8a2d1d; --soft:#e7e2d8; }
* { box-sizing: border-box; }
body { margin:0; font: 17px/1.65 Georgia, 'Times New Roman', serif; color: var(--ink); background: var(--paper); }
.wrap { max-width: 56rem; margin: 0 auto; padding: 0 1.2rem 4rem; }
header.site { background:#12312b; color:#f4f1ea; padding:.9rem 0; }
header.site .wrap { display:flex; gap:1rem; align-items:baseline; flex-wrap:wrap; padding-bottom:0; }
header.site .title { font-size:1.15rem; font-weight:bold; }
header.site a { color:#f4f1ea; text-decoration:none; }
.banner { background:#f3e7d8; border:2px solid var(--warn); color:#5c2115;
  font: 600 .92rem/1.5 'Helvetica Neue', Arial, sans-serif; padding:.6rem 1rem; margin:0 0 1.5rem; }
nav.docnav { display:flex; flex-wrap:wrap; gap:.4rem .9rem; padding:.6rem 1rem 1.4rem;
  font: .85rem 'Helvetica Neue', Arial, sans-serif; }
nav.docnav a { color:var(--accent); text-decoration:none; }
nav.docnav a:hover { text-decoration:underline; }
main h1 { font-size:1.7rem; line-height:1.25; }
h1,h2,h3 { font-family:'Helvetica Neue', Arial, sans-serif; }
pre { background:#12312b; color:#e9f3ef; padding:.9rem 1rem; overflow-x:auto; border-radius:.4rem; font-size:.9rem; }
code { font-family: 'SF Mono', Consolas, Menlo, monospace; }
p code, li code, th code, td code { background:var(--soft); padding:.05rem .3rem; border-radius:.25rem; font-size:.88em; }
blockquote { margin:0; padding:.7rem 1rem; background:#fdf2ee; border-left:5px solid var(--warn); }
blockquote p { margin:0; }
table { border-collapse:collapse; width:100%; margin:1rem 0; font-size:.95rem; }
th, td { border:1px solid #cfc8ba; padding:.4rem .6rem; text-align:left; vertical-align:top; }
th { background:var(--soft); }
li { margin:.25rem 0; }
footer.site { background:#eee9de; padding:1.4rem 0; font: .85rem 'Helvetica Neue', Arial, sans-serif; }
.pager { display:flex; justify-content:space-between; gap:1rem; margin-top:2.5rem;
  font: .95rem 'Helvetica Neue', Arial, sans-serif; }
.pager a { color:var(--accent); }
a { color:var(--accent); }
"""


def render_page(
    title: str,
    body_html: str,
    nav_html: str,
    pager_html: str,
    rel_prefix: str = "",
) -> str:
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{escape(title)} &mdash; {SITE_TITLE}</title>
<link rel="stylesheet" href="{rel_prefix}styles.css">
</head>
<body>
<header class="site"><div class="wrap"><span class="title"><a href="{rel_prefix}index.html">{SITE_TITLE}</a></span><span>by Asdale Dynamics, LLC</span></div></header>
<div class="banner">DISCLAIMER &mdash; {BANNER}</div>
<nav class="docnav">{nav_html}</nav>
<div class="wrap"><main>
{body_html}
<div class="pager">{pager_html}</div>
</main></div>
<footer class="site"><div class="wrap">
Every page of this manual is education for healthcare workers, not medical
advice, and never a substitute for facility policy or clinical judgment.
No patient data belongs in any AI tool. Built locally from Markdown files
in <code>docs/</code> and <code>samples/</code>; nothing was uploaded.
&copy; <a href="index.html">Asdale Dynamics, LLC</a> 2026 &middot; MIT License.
</div></footer>
</body>
</html>
"""


def find_pages(folders: dict[str, Path]) -> list[dict]:
    pages: list[dict] = []
    seen: set[Path] = set()
    for folder_name, folder in folders.items():
        if not folder.exists():
            continue
        for path in sorted(folder.glob("*.md")):
            if path.resolve() in seen:
                continue
            seen.add(path.resolve())
            slug = f"{folder_name}/{path.stem}" if folder_name else path.stem
            pages.append(
                {
                    "src": path,
                    "slug": slug,
                    "folder": folder_name,
                    "text": path.read_text(encoding="utf-8"),
                }
            )
    return pages


def section_order(pages: list[dict]) -> list[dict]:
    """Manual pages in reading order, then samples, then templates."""
    def sort_key(page: dict):
        name = page["src"].stem
        if name == "index":
            return (0, "", 0)
        num = re.match(r"^(\d\d)", name)
        return (1, name if num else name, 0)

    manual = [p for p in pages if p["folder"] == ""]
    samples = [p for p in pages if p["folder"] == "samples"]
    templates = [p for p in pages if p["folder"] == "templates"]
    ordered = sorted(manual, key=sort_key)
    numbered = [p for p in ordered if p["src"].stem != "index"]
    ordered = (
        [p for p in ordered if p["src"].stem == "index"]
        + sorted(numbered, key=lambda p: p["src"].stem)
        + samples
        + templates
    )
    return ordered


def build_site(out_dir: Path, roots: dict[str, Path] | None = None) -> list[Path]:
    """Build the full static site into out_dir; returns written file paths."""
    if roots is None:
        roots = {"": DOCS_DIR, "samples": SAMPLES_DIR, "templates": TEMPLATES_DIR}
    pages = find_pages(roots)
    if not any(p["src"].stem == "index" for p in pages):
        raise RuntimeError("no index.md found in docs/")

    ordered = section_order(pages)

    # source page path (relative to project root) -> output file name
    url_for: dict[Path, str] = {}
    for page in ordered:
        folder = page["folder"]
        if folder:
            subdir = folder + "/"
        else:
            subdir = ""
        url_for[page["src"].resolve()] = f"{subdir}{page['src'].stem}.html"

    def resolver_for_page(src_rel: Path, folder: str) -> Callable[[str], str | None]:
        def resolve(target: str) -> str | None:
            if target.startswith(("http://", "https://", "mailto:", "#")):
                return None
            base = src_rel.parent
            resolved_src = (base / target).resolve()
            url = url_for.get(resolved_src)
            if url is None:
                return None
            prefix = "" if not folder else "../"
            return prefix + url
        return resolve

    def nav_links(prefix: str) -> str:
        parts = []
        for page in ordered:
            url = url_for[page["src"].resolve()]
            label = re.sub(r"\s*\(.*\)\s*", "", extract_title(page["text"]))
            label = label.split(":")[0].strip()
            parts.append(f'<a href="{escape(prefix + url)}">{escape(label)}</a>')
        return " &middot; ".join(parts)

    written: list[Path] = []
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / "samples").mkdir(exist_ok=True)
    (out_dir / "templates").mkdir(exist_ok=True)

    for page in ordered:
        rel_src = page["src"].relative_to(ROOT) if page["src"].is_relative_to(ROOT) else page["src"]
        body = md_to_html(
            page["text"],
            link_resolver=resolver_for_page(rel_src, page["folder"]),
        )
        title = extract_title(page["text"])
        idx = ordered.index(page)
        prev_page = ordered[idx - 1] if idx else None
        next_page = ordered[idx + 1] if idx + 1 < len(ordered) else None
        pages_at_root = not page["folder"]
        prefix = "" if pages_at_root else "../"
        pager = ""
        if prev_page:
            prev_url = prefix + url_for[prev_page["src"].resolve()]
            pager += f'<span>&larr; <a href="{escape(prev_url)}">{escape(extract_title(prev_page["text"]))}</a></span>'
        else:
            pager += "<span></span>"
        if next_page:
            next_url = prefix + url_for[next_page["src"].resolve()]
            pager += f'<span><a href="{escape(next_url)}">{escape(extract_title(next_page["text"]))}</a> &rarr;</span>'
        else:
            pager += "<span></span>"
        html_page = render_page(title, body, nav_links(prefix), pager, rel_prefix=prefix)
        dest = out_dir / url_for[page["src"].resolve()]
        dest.write_text(html_page, encoding="utf-8")
        written.append(dest)

        raw_md = page["text"]
        raw_dest = dest.with_suffix(".md.txt")
        raw_dest.write_text(raw_md, encoding="utf-8")
        written.append(raw_dest)

    stylesheet = out_dir / "styles.css"
    stylesheet.write_text(STYLESHEET, encoding="utf-8")
    written.append(stylesheet)

    return written


def escape(text: str) -> str:
    return html.escape(text, quote=True)


def main() -> int:
    parser = argparse.ArgumentParser(description="Build the patient-teaching manual site.")
    parser.add_argument("--out", default=str(DEFAULT_OUT), help="output directory (default: site/)")
    parser.add_argument("--check", action="store_true", help="verify site is up to date; do not write to --out")
    args = parser.parse_args()

    out_dir = Path(args.out).resolve()
    if args.check:
        fresh_root = ROOT / ".build-check"
        if fresh_root.exists():
            shutil.rmtree(fresh_root)
        try:
            built = build_site(fresh_root)
            for path in built:
                rel = path.relative_to(fresh_root)
                existing = out_dir / rel
                if not existing.exists():
                    print(f"check: missing {existing}", file=sys.stderr)
                    return 1
                if existing.read_bytes() != path.read_bytes():
                    print(f"check: stale {existing}", file=sys.stderr)
                    return 1
            print(f"check: {out_dir} is up to date")
            return 0
        finally:
            if fresh_root.exists():
                shutil.rmtree(fresh_root)
    try:
        written = build_site(out_dir)
    except (OSError, RuntimeError) as exc:
        print(f"build: {exc}", file=sys.stderr)
        return 1
    print(f"built {len(written)} files in {out_dir}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
