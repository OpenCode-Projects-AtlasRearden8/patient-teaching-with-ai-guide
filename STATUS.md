# STATUS.md — Project Status

**Project:** Patient Teaching with AI — A Healthcare Worker's Manual
**Owner:** Asdale Dynamics, LLC (Dylan Asdale)
**Last verified:** 2026-10-25

> **DISCLAIMER — EDUCATION ONLY, NEVER MEDICAL ADVICE.** This whole project is
> education for healthcare workers about AI-assisted drafting of
> patient-education handouts. It is not medical advice and never a substitute
> for facility policy, clinical review, or licensed judgment. No patient data
> appears anywhere in this repository, and no AI tool should ever receive
> patient data. All handout samples are fabricated teaching material.

## What was built

1. **A complete beginner manual (Markdown, `docs/`)** — 12 documents: welcome,
   the always-on disclaimer, safe/local-first setup, the 4-D drafting workflow
   (Define → Draft → De-AI → Detail), readability measurement and fixing,
   teach-back patterns, AI-error spotting (five predictable error buckets with
   per-bucket checks), a facility-policy clearance checklist, copyright-safe
   reuse rules, annotated before/after rewrites, an eight-script prompt
   library, and a plain-words glossary. Every document carries the
   education-only disclaimer.
2. **`build.py`** — a dependency-free (Python standard library only) static
   site generator that turns `docs/`, `samples/`, and `templates/` Markdown
   into a styled HTML site in `site/` with a page banner disclaimer, nav, and
   prev/next pager on every page, plus raw `.md.txt` copies for offline use.
   `--check` mode verifies the built site is fresh.
3. **`tools/readability.py`** — an offline readability checker (Flesch Reading
   Ease, Flesch-Kincaid grade, long-sentence detection) with a `--target`
   PASS/FAIL gate (grade 8.0 or easier; FRE ≥ 60) and nonzero exit on failure
   so it can gate scripts. Pure stdlib; reads files or stdin.
4. **`templates/`** — print-ready pre-print checklist card and a fill-in
   handout skeleton.
5. **`samples/`** — four fabricated teaching samples (sunburn and child-fever
   handouts, "before" and "after" versions) demonstrating the workflow; the
   rewrites pass the readability gate, the originals fail by design.
6. **`tests/` (pytest, 24 tests)** — readability math, markdown→HTML builder
   behavior, full site assembly and cross-page links, disclaimers present in
   every manual file, no secret-looking strings, no PHI-shaped patterns,
   samples flagged as fabricated, exact LICENSE copyright line, and README
   credit.

## How to run it

```bash
# Build + check the site (first time and after edits; needs Python 3.10+)
python3 build.py
python3 build.py --check

# Read the site locally (no network involved)
python3 -m http.server 8000 --directory site
# open http://localhost:8000

# Check reading level of a draft (education-only wording check)
python3 tools/readability.py --target samples/handout-rewritten.md

# Run the test suite
python3 -m pytest tests/ -q
```

Everything runs locally: no accounts, no API keys, no patient data, no
network calls in any tool, and nothing is ever pushed or published by these
commands.

## Verification results (all run 2026-10-25)

| Check | Command | Result |
|---|---|---|
| Test suite | `python3 -m pytest tests/ -q` | **24 passed** |
| Site build | `python3 build.py` | **37 files** written to `site/` |
| Freshness check | `python3 build.py --check` | `site is up to date` (exit 0) |
| Readability gate (rewrites) | `python3 tools/readability.py --target samples/handout-rewritten.md samples/fever-rewritten.md` | **PASS** (FKGL 5.3 / 5.8; FRE 76.2 / 74.9) |
| Readability gate (originals) | `... --target samples/handout-original.md samples/fever-original.md` | **FAIL by design** (FKGL 20.4 / 17.2) — exit code 1 works as a gate |
| Readability CLI (stdin) | `echo ... \| python3 tools/readability.py -` | works |
| Byte-compile of all Python | `python3 -m py_compile build.py tools/readability.py tests/*.py` | clean |
| Git | `git log --oneline` | 1 commit, plain message, no co-author trailers |
| Disclaimers | test-enforced | every docs/samples/templates file passes |
| Secrets/PHI scan | test-enforced | clean |

## Known gaps / future work

- **Readability math is heuristic English**: a small exception table covers
  common problem words; unusual multisyllable words may count slightly off.
  Fine as a smoke alarm, not as an official measure.
- **Markdown coverage**: the converter handles the manual's feature set
  (headings, lists incl. checkboxes, tables, fenced code, blockquotes,
  emphasis, links) but not nested blockquotes or deep list nesting — add
  features only when the manual needs them (tests cover each feature added).
- **Single-language**: readability scoring assumes English.
- **No visible page creating/preflight app UI**: the deliverable is manual + site
  + checker by design (this scope), not a write-protect review app.
- **Site is git-ignored**: rebuild with `python3 build.py` after any clone.
- **Accessibility polish** (focus states, print CSS) could be deepened.
