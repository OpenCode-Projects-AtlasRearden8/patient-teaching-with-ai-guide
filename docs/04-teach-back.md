# Teach-Back: The Test That Is Not a Test

> **DISCLAIMER — EDUCATION ONLY, NEVER MEDICAL ADVICE.** Teach-back is a
> communication-quality check for education, not a clinical assessment, and it
> never substitutes for a clinician's evaluation. **Never put patient data into
> any AI tool** — including teach-back conversations from a real patient; use
> role-play examples only.

## What teach-back is

Teach-back closes the loop: after you teach, the patient (or family member)
explains the plan **in their own words**. You are evaluating *your teaching*
and *the handout* — never them, never memory, never "did you pass."

A patient's confusion after teach-back is data about the handout and the
explanation. That is the entire mindset.

The phrase to use, verbatim if helpful:

> "I want to make sure I explained this well. Can you tell me how you'll take
> this medicine, in your own words?"

Never: "Do you understand?" (yes is the only exit), "What did I just say?"
(quizzing), "Were you listening?" (never).

## Where AI fits: writing the prompts, not grading people

AI cannot and must not grade anyone's understanding. What it can do well:

1. Draft **teach-back prompt questions** keyed to each "what to do" step.
2. Draft **role-play scenarios** for staff training.
3. Draft **"if the answer misses the point" conversation starters** for the
   coach (you) — i.e., what to re-teach, in plain words.

## Pattern 1 — One teach-back question per action

Give the AI your finished handout's action list, and ask for one question per
step, locked to the handout's own wording:

```text
Education only, not medical advice; will be reviewed by clinical staff.

Below is a patient-education handout. For each numbered "what to do" step,
write ONE teach-back question it would let a patient answer in their own
words. Rules:
- The question must be answerable using ONLY the handout.
- Use plain words at a 6th-grade level.
- Never ask "do you understand"; ask them to describe or show.
- No new medical facts. If a step contains none, say so.

HANDOUT:
<paste approved handout>
```

Old rule from chapter 02, same muscle: the AI writes questions from your
approved facts; it never invents content.

## Pattern 2 — Role-play for staff training

For unit in-services and AI-literacy half-days, a scripted patient saves
setup time (and a stranger):

```text
Education only. Write a role-play script for staff teach-back practice.

Scenario: adult patient, no medical background, just told they need to
manage [GENERIC CONDITION] at home. The patient is friendly, forgets
details under stress, and mixes up step 2 and step 3.

Script the PATIENT ONLY, not the nurse. Patient lines must be realistic
confusions, not quiz answers. Leave the nurse's lines blank as [NURSE].
```

Never name, echo, or paste anything from a real patient encounter. De-identified
means *you* cannot recognize them either.

## Pattern 3 — Missed-point coaching phrases

Ask the AI for re-teaching openers you can grab when a teach-back answer
misses the point:

```text
Give me 5 short, kind phrases a nurse can say when the patient's
teach-back misses the point of handout step 1. Each phrase must:
- Put the miss on the explanation, never the patient.
- Invite a retry ("Let me try again a different way...").
- Stay under 15 words.
```

Training module? Run these once and keep winners in the unit shared drive.

## The 90-second unit workflow

1. **Teach** with the approved handout, pointing at each block as you go.
2. **Ask one** teach-back question — the one keyed to the step that matters
   most today (usually the "when to worry" line).
3. **Miss?** Re-teach that one step differently — different words, not louder
   or slower — and ask again, once.
4. **Second miss?** Flag the handout wording; that is a fixable class of
   problem. Note the exact step for the education committee.
5. **Document per policy** the education event and any follow-up — not the
   patient's quoted words, not a grade, not a "comprehension score."

## Red flags in AI-drafted teach-back questions

Delete or rewrite any question that is:

- **Closed** — answerable with yes/no, which teach-back cannot use.
- **Loaded** — "understands" baked into the wording.
- **Vocab trap** — a question that explains using the same jargon the patient
  may not know.
- **Off-handout** — mentions a fact that is not on the sheet; now you are
  teaching something nobody approved.
