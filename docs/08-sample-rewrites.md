# Sample Rewrites: Before and After, Annotated

> **DISCLAIMER — EDUCATION ONLY, NEVER MEDICAL ADVICE.** These samples are
> fabricated teaching examples about common, low-risk topics; they are not
> clinical instructions for any patient and not a substitute for approved
> sources. In a real facility the topics, wording, and "call now" lines would
> come from your approved library. **Never put patient data into any AI tool.**

Two full rewrites, annotated line by line, using the 4-D workflow from
[02-drafting-handouts.md](02-drafting-handouts.md) and the checks from
[05-spotting-ai-errors.md](05-spotting-ai-errors.md). The original and rewritten files live in
`samples/` so you can run the readability checker on each stage yourself.

## Sample 1: Sunburn care (fabricated teaching sample)

**Audience:** adults, general public. **Goal:** one page, grade 6–8.

Before (written in the classic tangle — the samples show the *typical* case,
not the worst case), annotated:

```text
"Patients sustaining actinic injury should maintain adequate cutaneous
hydration via emollient application.
```
- One 13-word sentence doing one job, but in the wrong vocabulary for the
  audience: four clinical words where two plain ones would do.
- Passive voice "should be applied" turns an instruction into weather.

After (the samples' rewritten file, annotated):

```text
Caring for Your Sunburn at Home

Put aloe vera gel on the burn 2-3 times a day.
This cools the skin and helps it feel better.
```
- **Verb-first steps** — the patient knows exactly what to do, in order.
- **"2-3 times a day"** — kept because our fabricated teaching facts include
  it AND the Source line names where it came from; in a real facility, this
  would trace to the approved library item (check #1, chapter 05).
- **One job per step** — aloe is separate from hydration is separate from meds.
- "Why it helps" a.k.a. the *motivation line* — a single short sentence that
  teaches rather than lectures; it is what the reader remembers when they
  have forgotten the number.

The compare command:

```bash
python3 tools/readability.py --target samples/handout-original.md samples/handout-rewritten.md
```

Both rewrites pass --target: grade 5.3 and 5.8, FRE 76.2 and 74.9 (easier
than grade 6 is fine — the pass bar is grade 8 or easier and FRE 60+). Run
this comparison on each revision so you can watch numbers drop as sentences
shorten.

## Sample 2: Fever in children (fabricated teaching sample)

This one demonstrates the **fact-trace discipline**, because fever handouts
carry the highest-risk lines in family education: what temperature means
"call now."

The rewrite sequence, annotated by the stage of the pipeline:

1. **Define step (human facts, from memory only):** dose-by-weight and
   else-phone-triage lines — and then **stop the AI from adding any numbers**.
   In the sample prompts (chapter 02) the "do not add medical facts" clause is
   doing exactly this work.
2. **Draft step (AI wording):** short sentences, verb-first, plain words.
3. **De-AI step (diff):** the most common failure mode this catches is the AI
   rounding or re-stating a dose or threshold "helpfully." In the samples, the
   rewritten file has dose/threshold numbers only in lines marked as coming
   from the teaching source. In a real facility your numbers come from your
   approved sources, full stop — never from the model.
4. **Detail step (read aloud):** the "when to call" block in the rewritten
   sample uses the pattern **specific trigger + action**: " Trouble breathing;
   bluish lips; can't wake up → call 911 now." A symptom a parent can *see*,
   followed by a thing they *do*.

## What both rewrites have in common

- **The "call now" block survived everything.** When content pressure mounts,
  it is the one block never cut.
- **Zero encounter-specific phrasing** — reusable anywhere, per the check in
  chapter 05, and compliant with the privacy habit of drafting at the
  condition level.
- **The footer** names: source, "Education only," reviewer, approval date, and
  the AI-assist line. It is the chapter-03 footer pattern, applied.
- **Score:** both rewritten samples pass the bundled tool's --target check
  (grade 8 or easier, FRE 60+; they land near grade 5–6 — easier is fine).
  Run the batch and read the verdicts — the two "original" files report
  FAIL by design (they are the before state):

```bash
python3 tools/readability.py --target samples/*.md
```

If your facility adopts nothing else from this manual, adopt the blocking
checklist (chapter 06) and the "call now" rule: it is the page's single most
used block, and a missing one is the kind of failure nobody sees until it
matters.
