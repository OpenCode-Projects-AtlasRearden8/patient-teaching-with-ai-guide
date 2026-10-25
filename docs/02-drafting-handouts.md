# Drafting Handouts: From Blank Page to Readable Draft

> **DISCLAIMER — EDUCATION ONLY, NEVER MEDICAL ADVICE.** This chapter shows a
> drafting workflow; it does not supply clinical content. Every clinical fact —
> yours or the AI's — must be verified against approved sources and cleared by
> your facility before printing. **Never put patient data into any AI tool.**

## What a good handout actually is

A patient handout is not a discharge summary for civilians. It is a one-page
(or less) answer to: **"what do I need to do when I get home, and when do I
worry?"** Good handouts share a skeleton:

1. **Headline in the patient's words** — "Caring for your sunburn at home"
   beats "Actinic injury: patient information."
2. **What it is**, in two or three plain sentences.
3. **What to do** — 3–6 numbered actions, each one step, each starting with a verb.
4. **What to avoid** — short, concrete, no hedging.
5. **When to call / go now** — specific, action-triggering symptoms and a number to call.
6. **Where we got this** — source line and approval line (see
   [07-copyright-safe-reuse.md](07-copyright-safe-reuse.md)).

If your draft does not have all six blocks, it is not finished — whatever the
AI says.

## The 4-D workflow: Define, Draft, De-AI, Detail

### 1. Define (before any AI)

Write in your own words, on paper or in the editor:

- The condition in one line.
- The three behaviors a patient must get right.
- The two symptoms that mean "call now."
- The audience: age band, assumed reading level, stress level.

If you cannot do this step from memory without opening a chart, you are too
close to a specific patient to draft safely. Genericize first.

### 2. Draft (AI's job, constrained)

Use a prompt that locks the AI to your facts. The core pattern:

```text
You are helping a nurse write a patient-education handout. It must be
education, not medical advice, and will be reviewed by clinical staff.

RULES:
- Use ONLY the facts in my draft below. Do not add, infer, or complete
  any medical fact. If information is missing, ask me, do not invent it.
- Write for a 6th-grade reader: short sentences (under 15 words where
  possible), everyday words, one idea per sentence.
- No jargon without a plain-word definition on first use.
- Never address a specific patient. No "you were given..." phrasing.
- End with "Approved by: ____  Date: ____".

MY DRAFT (my facts):
<paste your Define-step notes>
```

Why this works: the single biggest source of handout errors is **AI-added
facts** — a dose, a duration, a threshold invented to fill the page. Locking
the facts and demanding questions instead of additions moves the AI's effort
to wording, where it is actually good.

### 3. De-AI (your first read: hunt additions)

Diff the output against your Define notes:

- **Every clinical fact must trace to a source.** Yours, an approved
  handout, or a guideline document your facility endorses. If the AI
  introduced it — even a plausible-looking "drink 8 glasses" — either verify
  it against an approved source or delete it.
- **Tone check:** remove any line that sounds like the handout is diagnosing,
  prescribing, or addressing one person's situation.
- **Length check:** if the handout grew, figure out why. AI pads. Padding
  dilutes the "when to worry" line, which is the line patients actually need.

### 4. Detail (your second read: hunt friction)

Read it aloud, at the speed you would give instructions to a tired person at
11 p.m. Mark every stumble:

- Sentences over ~15–20 words → split.
- Any word a patient would define differently than we do ("ambulate," "NPO,"
  "intact") → replace or define.
- Passive voice ("medication should be taken") → active ("take your pill at 8 a.m.").
- Numbered steps with more than one comma inside → likely two steps.

Then run the readability check:
[03-readability-checks.md](03-readability-checks.md) explains the numbers; `tools/readability.py`
does the math. Target grade 6–8; if it reads above that, the fix is almost
always splitting sentences and swapping vocabulary, both of which chapter 03
walks through.

## Structure templates that AI fills well

AI handles **fixed skeletons** better than free-form requests because the
structure comes from you, and the model only spends its effort on wording:

```text
CARING FOR [CONDITION] AT HOME

What it is: [2 plain sentences]

What to do:
1. [one action]
2. [one action]
3. [one action]

What NOT to do:
- [avoidance, concrete]

Call your clinic if: [symptom, symptom, symptom]
Go to the ED / call 911 now if: [severe symptom]

This sheet is for education only. It does not replace advice from
your care team.

Approved by: ____  Date: ____  Source: ____
```

Give the AI the skeleton with your facts slotted in and ask it only to
"rewrite for clarity at a 6th-grade level, changing no facts." The verify step
(De-AI) is then mostly reading for wording, with a quick fact-trace pass.

## What AI is genuinely good at here

Be fair to it — done this way, AI is excellent at:

- **Vocabulary leveling**: replacing "hydration" with "enough fluids," per your gloss.
- **Splitting run-ons and enforcing the 15-word sentence budget.**
- **Consistent step formatting** and parallel verb-first steps.
- **Itself spotting hard words**: "List any words in this draft a reader
  without medical training might not know, and suggest plainer swaps."

## What AI is bad at here (assume until verified)

- **Any number attached to medicine**: doses, times, counts, thresholds,
  durations. Verify or delete.
- **Drug names and brand/generic pairs.** It mixes them confidently.
- **"When to worry" thresholds** — the most dangerous line in the handout.
- **Citations.** It will cite guidelines that do not exist. Assume fabricated
  until you click or look it up yourself.

Chapter [05-spotting-ai-errors.md](05-spotting-ai-errors.md) turns this into a full pre-print
checklist.
