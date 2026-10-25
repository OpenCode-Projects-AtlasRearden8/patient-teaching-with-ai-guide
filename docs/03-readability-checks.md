# Readability Checks: Grade 6–8, and How to Get There

> **DISCLAIMER — EDUCATION ONLY, NEVER MEDICAL ADVICE.** Readability scoring is
> about wording and sentence length, not clinical correctness. A readable wrong
> handout is still wrong. Verify facts (see [05-spotting-ai-errors.md](05-spotting-ai-errors.md))
> before anything reaches paper. **Never put patient data into any AI tool.**

## Why we measure

Most health-literacy guidance for adult patients targets a **6th– to 8th-grade**
reading level. That is not a judgment of patients; it is physics of the
room: people reading medical handouts are often tired, stressed, carrying a
new diagnosis, and reading English as a second or third language. Clear
wording is the highest-leverage kindness available.

"Measuring" beats "feeling clear" because clinicians consistently overestimate
the readability of text they wrote. The number does not lie; the sentence does.

## The three numbers in this manual's checker

The bundled tool `tools/readability.py` computes, from plain text:

- **Flesch Reading Ease (FRE)** — a 0–100 scale where *higher is easier*.
  Health handouts should aim for roughly **60–80**; adults understand best
  around the top of that band. The tool's pass bar is FRE 60 or higher.
- **Flesch-Kincaid Grade Level (FKGL)** — the same idea as a school grade.
  Target **6.0–8.0**.
- **Average words per sentence** and **long-sentence count** — the two levers
  you actually pull to fix a score.

Both Flesch formulas come from the same inputs — average sentence length and
average syllables per word — so they always move together:

- FRE ≈ 206.835 − 1.015 × (words/sentence) − 84.6 × (syllables/word)
- FKGL ≈ 0.39 × (words/sentence) + 11.8 × (syllables/word) − 15.59

No network, no accounts, no keys — the tool is a few hundred lines of pure
Python you can read in one sitting (and audit, which is the point of
local-first).

## How to run it

From the project folder:

```bash
python3 tools/readability.py samples/handout-rewritten.md
```

Or text straight from stdin:

```bash
cat my-draft.md | python3 tools/readability.py -
```

Or ask for the strict grade-band report used in facility review:

```bash
python3 tools/readability.py --target my-draft.md
```

`--target` prints PASS/FAIL (grade 8.0 or easier, FRE 60+) and exits
nonzero on fail, so it can be wired into scripts later.

Interpreting a run (numbers below are illustrative):

```text
File:                    handout-rewritten.md
Words:                        310
Sentences:                     29   (avg 10.7 words/sentence)
Syllables:                    439   (avg 1.42 per word)
Long sentences (>20 words):   3   (longest: 26 words)
Flesch Reading Ease:         76.2   (must be >= 60; aim 60-80)
Flesch-Kincaid Grade:         5.3   (must be <= 8.0; aim 6-8.0)
Readability verdict:         PASS
```

## Reading the results: what to do with each failure

| Symptom | Meaning | First fix |
|---|---|---|
| FKGL above 8 | Sentences too long and/or heavy words | Split longest sentences; run the word-swap prompt in [09-prompt-library.md](09-prompt-library.md) |
| FRE below 60 | Same, worse | Same — and check for stacked clinical nouns ("medication administration directions") |
| Many >20-word sentences | Padded or stacked steps | One action per bullet |
| Score great but text still confusing | Structure problem, not wording | Chapter 02's six-block skeleton |

A high score is not a certificate. The checker measures wording; only a human
review determines whether the content is accurate, complete, and appropriate.

## The word-swap table (steal this)

AI is excellent at these swaps when asked explicitly. Keep this table next to
your draft and hand it to the model:

| Instead of... | Write... |
|---|---|
| ambulate | walk |
| NPO | nothing to eat or drink |
| hydration | enough fluids |
| medication administration | taking your medicine |
| adverse effect / iatrogenic | side effect |
| adequate/homeostasis | steady / stable, in plain words |
| utilize | use |
| commence/initiate | start |
| cephalalgia | headache |
| monitor | watch for |
| contraindicated | don't take if / your team may say no because |
| prognosis | what to expect |
| permissible | okay |
| prior to | before |
| subsequent to | after |
| experience dyspnea | have trouble breathing |
| wound dehiscence | the wound opening up |
| oral intake | eating and drinking |

## Worked micro-example

Before (a real-style, formula-heavy discharge block):

> "Patients should be advised to maintain adequate oral hydration and to
> ambulate frequently in the immediate post-procedural period to minimize the
> risk of thromboembolic complications."

After (FKGL measures easier than the original by a wide margin; run the
compare command below to see the real numbers for these files):

> "Drink plenty of water. Walk around often today. Moving helps prevent blood
> clots. Call us if your leg becomes painful, red, or swollen."

Same facts, three sentences shorter, and the "call us" line finally on the page.
Run both through the checker in one command to see the gap for yourself:

```bash
python3 tools/readability.py samples/handout-original.md samples/handout-rewritten.md
```

## A note on honesty about limits

Readability formulas are the cheapest useful smoke alarm, not a quality
certificate. They ignore layout, fonts, illustrations, reading order, and —
most importantly — whether the *content* is right. Treat them like a pulse
oximeter: a sudden bad number means look at the patient; a good number does
not mean go home.
