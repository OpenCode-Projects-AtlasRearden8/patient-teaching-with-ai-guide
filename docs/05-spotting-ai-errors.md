# Spotting AI Errors Before They Reach Paper

> **DISCLAIMER — EDUCATION ONLY, NEVER MEDICAL ADVICE.** This chapter is your
> pre-print safety net; it is not a clinical review and never replaces one.
> Only a qualified reviewer plus your facility's approval process can clear a
> handout. **Never put patient data into any AI tool.**

## The core idea: AI errors are predictable

Language models do not "research." They write text shaped like answers. Most
failures fall into five repeatable buckets — and every bucket has a specific
check you can run in seconds.

| Bucket | What it looks like | Pre-print check |
|---|---|---|
| 1. Invented fact | A dose, count, threshold, or duration not in your source | Trace every number to an approved source |
| 2. Fabricated citation | "per the 2021 CDC guideline" — which may not exist | Click or look up every source it names |
| 3. Wrong de-identification | "As discussed..." phrasing that implies a specific patient | Grep for "you were," "your chart," "as discussed" |
| 4. Hedged instruction | "Typically you might consider possibly..." | Undecided instructions fail review |
| 5. Stale info | Out-of-date guidance stated confidently | Check the date on anything treatment-guided |

## The five checks, one by one

### Check 1 — Trace every number

Print the draft and draw a line under each number: doses, days, counts,
temperatures, thresholds, percentages, "8 glasses," "within 24 hours." For each:

- Is the number in **your** Define-notes (chapter 02) or an **approved source**
  you can name in the footer's Source line?
- If it came only from the AI, delete it or verify it. There is no third option.

> A handout with a wrong number is not a typo; it is an instruction someone
> trusts. Numbers are the highest-risk text in the document.

### Check 2 — Hunt the sources

Ask the AI explicitly, in the same session:

```text
List every source, guideline, organization, or publication you relied on
for anything in the draft above.
```

Then:

- Any source you cannot open or find in your facility's library → delete the
  content attached to it, or replace the content with an approved source.
- Never let the AI cite things for you; cite from sources you read.

### Check 3 — Strip anything patient-shaped

Search the draft (Ctrl+F) for:

- "as discussed", "as you were told", "your procedure", "your medication(s)",
  "when you were discharged", "your chart/records"
- Any pronoun usage that presumes a specific encounter

The fix is generic phrasing: "take the medicine your care team prescribed."
A handout is a **reuse-anywhere document**; anything encounter-shaped needs to go.

### Check 4 — Kill hedged instructions

Search for: "typically," "generally," "may want to consider," "somewhat,"
"often," "it is common to." Hedging is how the AI talks when it does not know.
Where you need a clear instruction, get the actual rule from an approved
source and write it plainly; where genuine uncertainty exists, route it to
the care team: "ask your care team whether ___ applies to you."

### Check 5 — Date-stamp and staleness-check

Ask the AI: "What is the most recent date of the information you used?"
Then write the date in the footer regardless:

```text
Reviewed: 2026-11-02 by J. Doe, RN, BSN
Source: facility handout #4412 (rev. 2026-08)
Drafted with AI assistance; human-reviewed before approval.
```

The footer line "Drafted with AI assistance; human-reviewed" is honest,
one line, and protects the review process you actually ran — including on the
days when the honest answer is "AI drafted it and I checked every line."

## The 60-second "stop anything" scan

Before printing, run these three questions against the draft with fresh eyes:

1. **Can I point to a source for every fact?** If no: stop.
2. **Would I be comfortable if this exact sheet went to a family member?**
   (Familiarity catches tone and clarity misses that a checklist misses.)
3. **Does the "call now" line exist, is it specific, and is the number right?**
   The single most-used block on the sheet; a missing one is a systemic fail.

## Escalation ladder

| Situation | Who reviews |
|---|---|
| Routine wording polish of an already-approved topic | You + second nurse/educator |
| Any new clinical content, number, or threshold | Clinical educator or content owner |
| New topic not in your facility's library | Clinical content specialist/committee |
| Anything that contradicts an approved source | Stop; escalate before another word is written |

If your facility has a patient-education committee, route AI-assisted drafts
through the same door as human drafts — with the footer line noting the
assist. If unsure whether something needs the committee, it does.
