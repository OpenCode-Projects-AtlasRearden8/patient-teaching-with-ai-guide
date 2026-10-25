# Patient Teaching with AI: A Healthcare Worker's Manual

> **DISCLAIMER — EDUCATION ONLY, NEVER MEDICAL ADVICE.** Everything in this
> repository — the manual, the checklists, the samples, the tools — is
> education for healthcare workers about how to draft plain-language
> patient-education handouts with AI assistance. It is not medical advice,
> not clinical guidance, and never a substitute for your facility's policies,
> your scope of practice, or a licensed clinician's judgment. **Never put
> patient data into any AI tool.**

A beginner-friendly, warm, step-by-step manual by [Asdale Dynamics, LLC]
(#copyright) for nurses, techs, therapists, and unit-based champions who want
patient handouts people can actually read — written "like a friend would."

## What's inside

| Path | What it is |
|---|---|
| `docs/index.md` | Welcome page: who this is for, the five rules |
| `docs/00-disclaimer.md` | The education-only disclaimer (meaning it) |
| `docs/01-getting-started.md` | A safe, local-first AI drafting setup |
| `docs/02-drafting-handouts.md` | The 4-D drafting workflow (Define, Draft, De-AI, Detail) |
| `docs/03-readability-checks.md` | Measuring and fixing readability (grade 6–8) |
| `docs/04-teach-back.md` | Teach-back prompts and patterns |
| `docs/05-spotting-ai-errors.md` | Catching AI errors before they reach paper |
| `docs/06-facility-policy-checklist.md` | Clearing the handout with your facility |
| `docs/07-copyright-safe-reuse.md` | Reusing and adapting sources without copyright trouble |
| `docs/08-sample-rewrites.md` | Annotated before/after rewrites |
| `docs/09-prompt-library.md` | Copy-paste prompts that already embody the rules |
| `docs/10-glossary.md` | Plain-words glossary |
| `templates/` | Print-ready pre-print checklist and handout skeleton |
| `samples/` | Fabricated teaching samples (before/after handout rewrites) |
| `tools/readability.py` | Offline readability checker (Flesch Reading Ease, Flesch-Kincaid) |
| `build.py` | Builds the static HTML site from docs/ — no dependencies |
| `site/` | The built site (generated; do not edit by hand) |

## Quick start

```bash
# Build the site (pure Python, no installs needed)
python3 build.py

# Read it locally
python3 -m http.server 8000 --directory site
# then open http://localhost:8000

# Check the reading level of any draft (education-only wording check)
python3 tools/readability.py --target samples/handout-rewritten.md
```

Or just read the Markdown in `docs/` — it is the manual, complete on its own.

## The five rules (they appear everywhere, on purpose)

1. Education only. Never medical advice.
2. No patient data in any AI tool, ever.
3. AI drafts; a qualified human verifies every claim; your facility approves.
4. Prove readability (grade 6–8 pass bar) with a check, not a feeling.
5. Teach back, don't hand out.

## Design commitments

- **Local-first.** No accounts, no keys, no network calls in any tool here;
  the site can be built and read entirely offline.
- **No patient data.** Nothing in the repo contains or processes any patient
  information; all samples are fabricated teaching material.
- **Tested.** The readability math, the markdown-to-HTML builder, and the
  content guarantees (disclaimers present, no secret-looking strings) are
  verified by a pytest suite in `tests/`.

## Run the tests

```bash
python3 -m pytest tests/ -q
```

## Republishing / credit

If this manual helps you, the credit line this project uses is:
**Asdale Dynamics, LLC** — plain-English AI education, books, and tools.

## Copyright

© **Copyright (c) 2026 Asdale Dynamics, LLC** — see [LICENSE](LICENSE) (MIT).
The upstream readability formulas (Flesch) are public-domain scholarship;
this implementation and all manual text are original work built for education.
