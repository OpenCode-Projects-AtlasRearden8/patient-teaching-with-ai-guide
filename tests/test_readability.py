"""Tests for the readability checker (education-only wording tool)."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "tools"))

from readability import (  # noqa: E402
    FRE_MIN,
    FKGL_MAX,
    LONG_SENTENCE_WORDS,
    count_syllables,
    count_words,
    passes_target,
    readability_stats,
    strip_markdown,
)

ROOT = Path(__file__).resolve().parent.parent


def test_syllable_counts_common_words():
    assert count_syllables("the") == 1
    assert count_syllables("walk") == 1
    assert count_syllables("hello") == 2
    assert count_syllables("reading") == 2
    assert count_syllables("table") == 2
    assert count_syllables("apple") == 2
    assert count_syllables("love") == 1
    assert count_syllables("time") == 1
    assert count_syllables("medicine") == 3


def test_word_counting_ignores_punctuation():
    assert count_words("Take your pill, at 8 a.m.") == 6
    assert count_words("") == 0


def test_strip_markdown_removes_code_blocks_and_quotes():
    text = (
        "# Title\n"
        "Paragraph one here.\n"
        "\n"
        "> Disclaimer note in a quote.\n"
        "\n"
        "```text\n"
        "code block content\n"
        "```\n"
        "\n"
        "- item one\n"
        "- [ ] item two\n"
    )
    plain = strip_markdown(text)
    assert "Disclaimer note" not in plain
    assert "code block content" not in plain
    assert "Paragraph one" in plain
    assert "item one" in plain
    assert "#" not in plain


def test_easy_text_passes_and_hard_text_fails():
    easy = (
        "Drink water. Walk a little every hour. "
        "Call the clinic if it gets worse. Sleep well tonight."
    )
    hard = (
        "Administration of pharmacotherapeutic agents in the postprocedural "
        "period necessitates vigilant monitoring for idiosyncratic "
        "hematological aberrations and for the exacerbation of previously "
        "documented comorbidities, in accordance with established "
        "institutional protocols and contemporary guidelines."
    )
    easy_stats = readability_stats(easy)
    hard_stats = readability_stats(hard)
    assert easy_stats["flesch_kincaid_grade"] < hard_stats["flesch_kincaid_grade"]
    assert passes_target(easy_stats)
    assert not passes_target(hard_stats)


def test_band_constants_match_the_manual():
    assert FRE_MIN == 60.0
    assert FKGL_MAX == 8.0


def test_stats_include_long_sentence_info():
    stats = readability_stats(
        "Short one. "
        "A very long sentence that keeps going and going beyond twenty words "
        "with plenty of filler phrases to pad the length out far past the "
        "line we set for handouts."
    )
    assert stats["long_sentence_count"] >= 1
    assert stats["longest_sentence_words"] > LONG_SENTENCE_WORDS


def test_sample_rewrites_pass_and_originals_fail():
    for original in ("handout-original.md", "fever-original.md"):
        text = (ROOT / "samples" / original).read_text(encoding="utf-8")
        stats = readability_stats(text)
        assert stats["flesch_kincaid_grade"] > FKGL_MAX, original
    for rewritten in ("handout-rewritten.md", "fever-rewritten.md"):
        text = (ROOT / "samples" / rewritten).read_text(encoding="utf-8")
        stats = readability_stats(text)
        assert passes_target(stats), rewritten
