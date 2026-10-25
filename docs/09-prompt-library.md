# The Prompt Library: Copy, Paste, and Use Today

> **DISCLAIMER — EDUCATION ONLY, NEVER MEDICAL ADVICE.** These prompts are
> workflow tools for education drafting; none of them manufactures clinical
> facts, none of them replaces review, and none of them should ever receive
> patient data. Your facility's policy decides which tool these may be typed
> into.

Every prompt below embodies the manual's core rule: **AI works only with the
facts you supply and says so when it can't.** Each one is copy-pasteable.

## 1. The Master Draft Prompt (the safe default)

```text
You are helping a nurse draft a patient-education handout. It is education,
not medical advice, and will be reviewed by clinical staff before use.

RULES (break any and I reject the draft):
- Use ONLY the facts in MY DRAFT below. Do not add, infer, or complete any
  medical fact. If information is missing, ASK me; never invent it.
- Write for a 6th-grade reader: short sentences (under 15 words where
  possible), everyday words, one idea per sentence.
- No jargon without a plain-word definition on first use.
- Never address a specific patient or encounter. No "as discussed" phrasing.
- Use this skeleton: title, "What it is", "What to do" (numbered,
  verb-first), "What NOT to do", "Call your clinic if", "Go now if",
  "This is for education only" line, "Approved by / Date / Source" lines.
- After the draft, list any words a lay reader might not know with a
  plainer swap for each.

MY DRAFT:
<paste your own notes — type them from memory, never from a chart>
```

## 2. The Readability Pass

```text
Rewrite the handout below for a 6th-grade reading level.

RULES:
- Change no facts. If you are not certain a sentence preserves the fact,
  leave it and ask me.
- Split sentences longer than 15 words into shorter ones.
- Swap clinical vocabulary for everyday words (list the swaps you made
  at the end).
- Keep every numbered step verb-first and one action only.
- Output the full handout, then a "CHANGES MADE" list.

HANDOUT:
<paste draft>
```

## 3. The Word-Trouble Hunter

```text
Below is a draft handout. List every word a reader without medical training
might not know. For each: give a plainer swap, or a 5-word definition.
Do not rewrite the draft; just the list.

DRAFT:
<paste>
```

## 4. The "What Did You Add?" Confession Prompt

```text
Compare MY DRAFT to your REWRITE above. List, line by line, anything in the
rewrite that was NOT in my draft - especially any number, dose, time,
threshold, or symptom. If the list is empty, say "No additions."
```

Keep this one for the end of every session; chapter 05's Check 1 becomes a
two-second read instead of a line-by-line hunt.

## 5. The Teach-Back Question Builder

```text
For each numbered "What to do" step in the handout below, write ONE
teach-back question the patient could answer in their own words.

RULES:
- Answerable using ONLY the handout.
- Open questions (describe / show me / tell me how), never yes/no.
- 6th-grade words.
- No new medical facts.

HANDOUT:
<paste approved handout>
```

## 6. The Role-Play Patient (staff training only)

```text
Write a role-play script for staff teach-back practice. Education only.

Scenario: adult patient, no medical background, friendly, forgets details
under stress, mixes up step 2 and step 3 of the sheet.

Script the PATIENT ONLY with realistic confusions, never quiz answers.
Leave the nurse's lines blank as [NURSE].
<paste handout>
```

## 7. The Pre-Print Red-Flag Scan

```text
Act as a patient-education reviewer. Education only. Given this draft,
flag anything that:
- is a clinical fact with no source named in the draft,
- names or implies a specific patient,
- uses hedged instructions ("typically", "may consider"),
- is missing the "when to call" block or has a vague one,
- is over grade 8 reading level.
Output a numbered list of problems only. Do not fix them; I will.

DRAFT:
<paste>
```

Use this *after* your manual checks, not instead of them — it is a second
net, not the first.

## 8. The Self-Critique Prompt

```text
Critique your own rewrite above as if you were a nurse educator checking
it against the rules you were given. List any rule you may have broken
and the sentence that breaks it. Be specific.
```

Models are decent critics of their own text once primed; you still verify
every output, but this catches drift you might skim past.

## Using the library well

- **One prompt at a time, in order** (draft → readability → confession →
  teach-back). Stacking them into one mega-prompt lowers quality noticeably.
- **Paste drafts, never context.** If the prompt needs a chart to make sense,
  your draft is at the wrong level of detail.
- **Keep sessions small.** A new session per handout keeps additions traceable.
- **Log the assist.** Footer line: "Drafted with AI assistance; human-reviewed".
