"""Content guarantees: disclaimers everywhere and no secrets/personal data."""

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

DISCLAIMER_HINTS = ("education only", "not medical advice", "never medical advice")

SECRET_PATTERNS = [
    re.compile(r"\bsk-[A-Za-z0-9_-]{10,}\b"),           # API-key style tokens
    re.compile(r"\bAKIA[0-9A-Z]{16}\b"),                 # AWS-style key ids
    re.compile(r"-----BEGIN [A-Z ]*PRIVATE KEY-----"),   # key material
    re.compile(r"\b(?:api[_-]?key|secret|token)\s*[:=]\s*['\"][A-Za-z0-9]{8,}", re.I),
]

PHI_PATTERNS = [
    re.compile(r"\bMRN[:\s]*#?\s*\d{4,}\b", re.I),
    re.compile(r"\b\d{3}-\d{2}-\d{4}\b"),                # US SSN shape
    re.compile(r"\b(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)?\.?\s*\d{1,2},?\s*\d{4}\s*,\s*room\s*\d+", re.I),
]


def every_md_file():
    for folder in ("docs", "samples", "templates", "tests", "tools"):
        yield from (ROOT / folder).rglob("*.md")
    for top in ("README.md", "STATUS.md"):
        path = ROOT / top
        if path.exists():
            yield path


def test_every_manual_file_carries_the_disclaimer():
    for path in list(every_md_file()):
        if path.name == "STATUS.md":
            continue  # status is a report file; hint checked separately
def _normalized(path: Path) -> str:
    lines = [line.lstrip("> ").lower() for line in path.read_text(encoding="utf-8").splitlines()]
    return re.sub(r"\s+", " ", " ".join(lines))


def test_every_manual_file_carries_the_disclaimer():
    for path in list(every_md_file()):
        if path.name == "STATUS.md":
            continue  # status is a report file; hint checked separately
        lowered = _normalized(path)
        assert any(h in lowered for h in DISCLAIMER_HINTS), f"no disclaimer: {path}"


def test_readme_carries_the_disclaimer():
    text = _normalized(ROOT / "README.md")
    assert "not medical advice" in text
    assert "never put patient data" in text


def test_no_secret_looking_strings_anywhere():
    patterns = list(SECRET_PATTERNS)
    path_names = [str(p) for p in ROOT.rglob("*") if p.is_file()]
    for path in path_names:
        if any(part in path for part in (".git/", "site/")):
            continue
        try:
            text = Path(path).read_text(encoding="utf-8", errors="ignore")
        except OSError:
            continue
        for pattern in patterns:
            assert not pattern.search(text), f"secret-like string in {path}"


def test_no_patient_identifier_patterns_in_manual_or_samples():
    for path in every_md_file():
        text = path.read_text(encoding="utf-8")
        for pattern in PHI_PATTERNS:
            assert not pattern.search(text), f"PHI-like pattern in {path}"


def test_samples_declared_fabricated():
    for path in (ROOT / "samples").glob("*.md"):
        assert "fabricated teaching example" in path.read_text(encoding="utf-8")


def test_license_line_exact():
    license_text = (ROOT / "LICENSE").read_text(encoding="utf-8")
    assert "Copyright (c) 2026 Asdale Dynamics, LLC" in license_text


def test_readme_credits_asdale_dynamics():
    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    assert "Asdale Dynamics, LLC" in readme
