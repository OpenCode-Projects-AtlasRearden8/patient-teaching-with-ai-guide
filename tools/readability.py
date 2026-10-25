#!/usr/bin/env python3
"""readability.py -- measure the reading level of patient-education drafts.

Education only. This tool measures wording (sentence length and syllable
density). It says nothing about clinical correctness. Never put patient
data into any tool.

Usage:
    python3 tools/readability.py FILE [FILE ...]
    python3 tools/readability.py -            # read from stdin
    python3 tools/readability.py --target FILE

--target prints PASS/FAIL against the manual's readability bar:
Flesch-Kincaid grade at grade 8.0 or easier (aim 6-8) and Flesch
Reading Ease at 60.0 or higher (aim 60-80), and exits nonzero if any
checked file falls short.

Pure standard library; runs offline.
Exit codes: 0 all pass, 1 fail, 2 usage/IO error.
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path
from typing import Iterable

FRE_MIN = 60.0
FKGL_MAX = 8.0
LONG_SENTENCE_WORDS = 20

# Common count-exceptions for the syllable heuristic. Checked lowercase
# and whole-word; anything not listed falls through to the vowel-group rule.
SYLLABLE_EXCEPTIONS = {
    "a": 1, "aloe": 2, "as": 1, "area": 2, "ai": 2, "bill": 1,
    "bread": 1, "business": 2, "children": 2, "come": 1, "came": 1,
    "care": 1, "done": 1, "every": 2, "fire": 1, "give": 1,
    "have": 1, "hello": 2, "here": 1, "hour": 1, "live": 1,
    "loose": 1, "medicine": 3, "move": 1, "physics": 2, "piece": 1,
    "pus": 1, "quiet": 2, "read": 1, "reading": 2, "room": 1,
    "said": 1, "same": 1, "send": 1, "site": 1, "size": 1,
    "some": 1, "state": 1, "text": 1, "the": 1, "theirs": 1,
    "there": 1, "these": 1, "those": 1, "time": 1, "water": 2,
    "where": 1, "wide": 1, "worry": 2, "your": 1,
}

VOWELS = "aeiouy"


def strip_markdown(text: str) -> str:
    """Reduce markdown to plain prose for scoring.

    Skips fenced code blocks and blockquote lines (editorial notes and
    disclaimers are not patient-facing body text), converts links to their
    label text, drops tables, and strips list/heading markers.
    """
    lines: list[str] = []
    in_fence = False
    for raw_line in text.splitlines():
        line = raw_line.rstrip()
        if line.lstrip().startswith("```"):
            in_fence = not in_fence
            continue
        if in_fence:
            continue
        stripped = line.strip()
        if stripped.startswith(">"):
            continue
        if stripped.startswith("|"):
            continue
        line = re.sub(r"!\[[^\]]*\]\([^)]*\)", "", line)
        line = re.sub(r"\[([^\]]*)\]\([^)]*\)", r"\1", line)
        line = re.sub(r"^\s*#{1,6}\s+", "", line)
        line = re.sub(r"^\s*[-*+]\s+(\[\s\]\s+)?", "", line)
        line = re.sub(r"^\s*\d+\.\s+(\[\s\]\s+)?", "", line)
        line = re.sub(r"^\s*[-*_]{3,}\s*$", "", line)
        line = re.sub(r"\*\*?|__?", "", line)
        line = re.sub(r"`([^`]*)`", r"\1", line)
        lines.append(line)
    return " ".join(lines)


WORD_RE = re.compile(r"[A-Za-z][A-Za-z'-]*")


def split_sentences(text: str) -> list[str]:
    text = re.sub(r"\s+", " ", text).strip()
    if not text:
        return []
    parts = re.split(r"(?<=[.!?;])\s+", text)
    return [p.strip() for p in parts if p.strip()]


def count_words(sentence: str) -> int:
    return len(WORD_RE.findall(sentence))


def count_syllables(word: str) -> int:
    """Heuristic English syllable count (vowel groups + known exceptions)."""
    w = word.lower().strip()
    w = re.sub(r"[^a-z]", "", w)
    if not w:
        return 0
    if w in SYLLABLE_EXCEPTIONS:
        return SYLLABLE_EXCEPTIONS[w]
    if len(w) <= 2:
        return 1

    body = w
    # "-ism" keeps its middle beat even after we count vowel groups.
    if w.endswith("ism"):
        body = w[:-3]

    # A final "-le" after a consonant is its own syllable ("table", "apple").
    if body.endswith("le") and len(body) > 2 and body[-3] not in VOWELS:
        stem, le_extra = body[:-2], 1
    elif body.endswith("e"):
        # Silent final "e" (as in "love", "time") adds no beat.
        stem, le_extra = body[:-1], 0
    else:
        stem, le_extra = body, 0

    groups = re.findall(rf"[{VOWELS}]+", stem)
    return max(1, len(groups) + le_extra)


def readability_stats(text: str) -> dict:
    plain = strip_markdown(text)
    sentences = [s for s in split_sentences(plain) if count_words(s) > 0]
    words = WORD_RE.findall(plain)
    syllables = sum(count_syllables(w) for w in words)

    n_sents = len(sentences)
    n_words = len(words)
    n_syll = syllables
    avg_words_per_sent = n_words / n_sents if n_sents else 0.0
    syll_per_word = n_syll / n_words if n_words else 0.0

    fre = (
        206.835 - 1.015 * avg_words_per_sent - 84.6 * syll_per_word
        if n_words and n_sents
        else 0.0
    )
    fkgl = (
        0.39 * avg_words_per_sent + 11.8 * syll_per_word - 15.59
        if n_words and n_sents
        else 0.0
    )
    long_sentences = [
        s for s in sentences if count_words(s) > LONG_SENTENCE_WORDS
    ]
    longest = max((count_words(s) for s in sentences), default=0)
    return {
        "words": n_words,
        "sentences": n_sents,
        "syllables": n_syll,
        "avg_words_per_sentence": avg_words_per_sent,
        "syllables_per_word": syll_per_word,
        "flesch_reading_ease": fre,
        "flesch_kincaid_grade": fkgl,
        "long_sentence_count": len(long_sentences),
        "longest_sentence_words": longest,
    }


def passes_target(stats: dict) -> bool:
    """Pass bar: grade 8.0 or easier (aim 6-8) and FRE 60+ (aim 60-80).

    Easier than grade 6 is a good thing for stressed readers, so the verdict
    has no lower bound on grade and no upper bound on FRE.
    """
    return (
        stats["flesch_reading_ease"] >= FRE_MIN
        and stats["flesch_kincaid_grade"] <= FKGL_MAX
    )


def format_report(label: str, stats: dict, target: bool) -> str:
    lines = [
        f"File:                    {label}",
        f"Words:                   {stats['words']:>10}",
        (
            f"Sentences:               {stats['sentences']:>10}"
            f"   (avg {stats['avg_words_per_sentence']:.1f} words/sentence)"
        ),
        (
            f"Syllables:               {stats['syllables']:>10}"
            f"   (avg {stats['syllables_per_word']:.2f} per word)"
        ),
        (
            f"Long sentences (>{LONG_SENTENCE_WORDS} words):"
            f" {stats['long_sentence_count']:>3}"
            f"   (longest: {stats['longest_sentence_words']} words)"
        ),
        (
            f"Flesch Reading Ease:     {stats['flesch_reading_ease']:>10.1f}"
            f"   (must be >= {FRE_MIN:.0f}; aim {FRE_MIN:.0f}-80)"
        ),
        (
            f"Flesch-Kincaid Grade:    {stats['flesch_kincaid_grade']:>10.1f}"
            f"   (must be <= {FKGL_MAX:.1f}; aim 6-{FKGL_MAX:.1f})"
        ),
    ]
    if target:
        verdict = (
            "PASS"
            if passes_target(stats)
            else "FAIL"
        )
        lines.append(f"Readability verdict:     {verdict:>10}")
    lines.append("")
    header = (
        "Output is a wording smoke alarm, not a quality certificate."
        " A good number is not clinical accuracy."
        if not target
        else ""
    )
    if header:
        lines.append(header)
    return "\n".join(lines)


def read_input(path: str) -> str:
    if path == "-":
        return sys.stdin.read()
    return Path(path).read_text(encoding="utf-8")


def main(argv: Iterable[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Education-only readability checker for draft handouts."
    )
    parser.add_argument("files", nargs="+", help="files to check, or '-' for stdin")
    parser.add_argument(
        "--target",
        action="store_true",
        help="print PASS/FAIL vs the grade 6-8 band; exit 1 on FAIL",
    )
    args = parser.parse_args(argv)

    if len(args.files) == 1 and args.files[0] in ("-"):
        try:
            text = read_input("-")
        except OSError as exc:
            print(f"readability: {exc}", file=sys.stderr)
            return 2
        stats = readability_stats(text)
        print(format_report("<stdin>", stats, args.target))
        if args.target and not passes_target(stats):
            return 1
        return 0

    status = 0
    for path in args.files:
        label = Path(path).name
        try:
            text = read_input(path)
        except OSError as exc:
            print(f"readability: cannot open {path}: {exc}", file=sys.stderr)
            status = 2
            continue
        stats = readability_stats(text)
        print(format_report(label, stats, args.target))
        if args.target and not passes_target(stats):
            status = 1
    return status


if __name__ == "__main__":
    sys.exit(main())
