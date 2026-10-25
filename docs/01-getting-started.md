# Getting Started: A Safe, Local-First AI Setup

> **DISCLAIMER — EDUCATION ONLY, NEVER MEDICAL ADVICE.** This chapter is about
> tooling and workflow, not clinical content. Everything here assumes **no
> patient data** enters any AI tool at any point, and that your facility's
> policy approves whatever tool you choose.

## The local-first principle

"Local-first" means: prefer tools and workflows that work without sending your
words to a third party, and fail gracefully without the internet. Two reasons:

1. **Privacy by habit.** If your workflow never involves pasting anything
   sensitive into a web box, you cannot accidentally leak it. The habit of
   writing a handout *from de-identified, condition-level knowledge* — never
   from a chart — is the safest habit in this manual.
2. **Offline resilience.** Units lose network access. A workflow built on a
   local text editor, a printed prompt library, and a readability script keeps
   working when the browser cannot.

## What you actually need

You need less than you think:

- **A text editor.** Any of them: Notepad, TextEdit (plain-text mode), VS Code,
  even a clipboard app. Markdown is the format this manual uses because it is
  plain text, easy to version, and readable even un-rendered.
- **An approved AI assistant**, in whatever form your facility permits. That
  might be an enterprise chat tool used with zero patient data, or a
  locally-installed model on a workstation. If it is neither, skip the AI
  drafting chapters and use this manual's templates by hand — they work on paper.
- **The readiness checker** in this repository (`tools/readability.py`), which
  measures reading level with plain Python. No account, no key, no network.
- **This manual** — printed or open in a browser.

## Choosing an AI tool: a three-question screen

Ask these three questions before you draft anything with a tool. If the answer
to any question is "no" or "unknown," do not use that tool for handout drafting.

1. **Am I allowed to?** Check your facility's AI/use policy (see
   [06-facility-policy-checklist.md](06-facility-policy-checklist.md)). Policy outranks
   everything, including your supervisor's enthusiasm.
2. **Could anything I type identify a patient?** If the tool ingests your text
   to improve its service, the bar for "safe to type" is even higher: nothing
   from a chart, nothing typed while remembering a specific patient. Draft at
   the level of the *condition*, not the *person*.
3. **Where does my text go?** Local model on a trusted machine: stays put.
   Enterprise tool with a business-associate-style agreement: governed.
   Free public website: assume your text is stored and possibly used. Never
   type anything you would not post on a break-room whiteboard — and even that
   bar is a floor, not a target.

## Local AI in one paragraph

Some AI models can run entirely on a hospital workstation or your own laptop:
you download the model once, and every conversation happens on the machine.
No text leaves the device. This is the simplest way to make "no data ever
leaves" true by construction. The trade-offs: models that fit on a typical
machine are less capable, slower, and still confidently wrong sometimes. The
verification chapters ([05-spotting-ai-errors.md](05-spotting-ai-errors.md)) apply fully to
local models. Local is a privacy feature, not a quality guarantee.

## Your first (safe) session: a dry run

Do this once before drafting anything real. It takes ten minutes and builds the
muscle memory that keeps patients safe later.

1. Pick a condition you know cold but that relates to **no patient you are
   currently caring for** — say, "sunburn" or "hiccups."
2. Write, from memory only, a five-sentence rough draft about what someone
   should know. No citations, no chart, no names.
3. Ask your AI tool: "Rewrite this for a reader at a 6th-grade level. Keep only
   the facts I gave you. Do not add any medical fact." (A version of this
   prompt is in [09-prompt-library.md](09-prompt-library.md).)
4. Compare draft and output. Highlight two things: (a) any fact the AI *added*
   that you did not supply — this is where errors live, and (b) any sentence a
   tired adult would still have to read twice.
5. Run `tools/readability.py` on the output and log the grade level.

You have now done the entire safe workflow in miniature: human facts in,
constrained rewrite, differential highlight, readability check. Chapters
[02](02-drafting-handouts.md)–[05](05-spotting-ai-errors.md) deepen each step.

## Setting up your workspace folder

Keep one folder for draft handouts, versioned like code. A simple starter:

```text
handouts/
  working/          <- AI drafts under review
  reviewed/         <- passed your read-through and readability check
  approved/         <- passed facility review; put approval date in filename
  archive/          <- superseded; keep for audit trail
```

Name files like `hand-foot-mouth-care-v3-2026-11-02-APPROVED.md`. The version
number, date, and approval status in the filename mean nobody ever prints a
stale draft by accident — one of the simplest and most effective safety
controls in this whole manual.

## Habits that prevent the classic mistakes

- **Draft from knowledge, never from records.** If writing it would require
  opening a chart, stop and use a generic condition-level draft instead.
- **Never paste, always type-from-memory.** Copy/paste is how private data
  jumps contexts; typing from memory keeps the draft at the right level of detail.
- **Keep the AI's additions visible.** Ask it to mark anything it added beyond
  your facts (prompt in [09-prompt-library.md](09-prompt-library.md)), then verify each addition or delete it.
- **Version every draft.** v1, v2, v3... with dates. See the naming rule above.
- **Log your reviews.** Two lines: what was checked, who approved it, when.
