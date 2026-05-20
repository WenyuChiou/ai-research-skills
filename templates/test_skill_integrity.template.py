"""Canonical integrity test for audit-first-skills bundles.

Copy this file as `tests/test_skill_integrity.py` in a sibling bundle repo.
Parameterized over every skill under `skills/<name>/`. Single source of truth
so future invariant changes propagate cleanly across sibling bundles.

Enforces:

  Mirror of academic-writing-skills/tests/test_skill_integrity.py:
    - Frontmatter (if present) is valid: name == directory, description non-empty
    - evals/evals.json shape: >=5 cases, unique ids, non-empty prompts
    - No mojibake markers in any *.md
    - Bilingual READMEs cross-reference each other

  The five audit-first invariants (see docs/audit-first-design.md):
    I1. AUDIT BUDGET   — SKILL.md <=350, references/<=8 files, recursive *.md <=2000
    I2. NO DECLARATIVE-ONLY GATES — no ARS_* env flags, no env.get() branches, no [TODO]
    I3. EVAL MIX       — at least one each of pos-/neg-/edge- id prefix
    I4. ANTI-HYPE README — bilingual `## Limitations` (EN) + `## 限制` (zh-TW) required
    I5. HONEST PROVENANCE — every ARS mention paired with a bracketed reference

Reference: docs/audit-first-design.md (the design contract this enforces).
"""

import json
import re
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
SKILLS_DIR = ROOT / "skills"
ALL_SKILLS = sorted(p.name for p in SKILLS_DIR.iterdir() if (p / "SKILL.md").exists())

assert ALL_SKILLS, f"no skills found under {SKILLS_DIR}"


def _read(p: Path) -> str:
    return p.read_text(encoding="utf-8")


# -----------------------------------------------------------------------------
# Mirror of academic-writing-skills/tests/test_skill_integrity.py
# -----------------------------------------------------------------------------

@pytest.mark.parametrize("skill", ALL_SKILLS)
def test_skill_md_frontmatter(skill):
    content = _read(SKILLS_DIR / skill / "SKILL.md")
    if not content.lstrip().startswith("---"):
        return  # frontmatter optional; if absent, nothing to validate
    fm = content.split("---", 2)[1] if content.count("---") >= 2 else ""
    name_m = re.search(r"^name:\s*(.+)$", fm, re.M)
    if name_m:
        assert name_m.group(1).strip() == skill, (
            f"{skill}: frontmatter name {name_m.group(1)!r} != directory name"
        )
    desc_m = re.search(r"^description:\s*(.+)$", fm, re.M)
    if desc_m:
        assert desc_m.group(1).strip(), f"{skill}: empty frontmatter description"


@pytest.mark.parametrize("skill", ALL_SKILLS)
def test_evals_shape(skill):
    p = SKILLS_DIR / skill / "evals" / "evals.json"
    assert p.exists(), f"{skill}: missing evals/evals.json"
    data = json.loads(_read(p))
    evals = data.get("evals", [])
    assert len(evals) >= 5, f"{skill}: only {len(evals)} evals; need >=5"
    ids = [e["id"] for e in evals]
    assert len(ids) == len(set(ids)), f"{skill}: duplicate eval ids"
    for e in evals:
        prompt = e.get("prompt", "")
        assert isinstance(prompt, str) and prompt.strip(), f"{skill}: empty prompt"


@pytest.mark.parametrize("skill", ALL_SKILLS)
def test_no_mojibake(skill):
    skill_dir = SKILLS_DIR / skill
    bad_markers = ["�"]
    for md in skill_dir.rglob("*.md"):
        text = _read(md)
        for b in bad_markers:
            assert b not in text, (
                f"{md.relative_to(ROOT)}: mojibake marker {b!r}"
            )


def test_bilingual_readmes_cross_reference():
    en = _read(ROOT / "README.md")
    zh = _read(ROOT / "README.zh-TW.md")
    assert "README.zh-TW" in en, "EN README must link to zh-TW counterpart"
    assert "README.md" in zh, "zh-TW README must link to EN counterpart"


# -----------------------------------------------------------------------------
# I1 — AUDIT BUDGET (the 30-min audit promise, made machine-checkable)
# -----------------------------------------------------------------------------

@pytest.mark.parametrize("skill", ALL_SKILLS)
def test_invariant_1_audit_budget(skill):
    skill_dir = SKILLS_DIR / skill
    skill_md_lines = len(_read(skill_dir / "SKILL.md").splitlines())
    assert skill_md_lines <= 350, f"I1 {skill}: SKILL.md {skill_md_lines} lines (>350)"

    refs = skill_dir / "references"
    if refs.exists():
        n_refs = sum(1 for _ in refs.glob("*.md")) + sum(1 for _ in refs.glob("*.json"))
        assert n_refs <= 8, f"I1 {skill}: references/ has {n_refs} files (>8)"

    total = sum(len(_read(p).splitlines()) for p in skill_dir.rglob("*.md"))
    assert total <= 2000, f"I1 {skill}: total markdown {total} lines (>2000)"


# -----------------------------------------------------------------------------
# I2 — NO DECLARATIVE-ONLY GATES (every claimed check is an assertion)
# -----------------------------------------------------------------------------

@pytest.mark.parametrize("skill", ALL_SKILLS)
def test_invariant_2_no_declarative_only_gates(skill):
    skill_dir = SKILLS_DIR / skill
    skill_md = _read(skill_dir / "SKILL.md")
    assert "ARS_" not in skill_md, f"I2 {skill}: ARS_* env flag in SKILL.md"
    assert "if env.get(" not in skill_md, f"I2 {skill}: env.get() runtime branch in SKILL.md"
    for md in skill_dir.rglob("*.md"):
        if "[TODO]" in _read(md):
            pytest.fail(f"I2 {md.relative_to(ROOT)}: unresolved [TODO] in shipped text")


# -----------------------------------------------------------------------------
# I3 — EVAL MIX (catches both false-negatives and false-positives)
# -----------------------------------------------------------------------------

@pytest.mark.parametrize("skill", ALL_SKILLS)
def test_invariant_3_eval_mix(skill):
    p = SKILLS_DIR / skill / "evals" / "evals.json"
    if not p.exists():
        pytest.skip(f"{skill}: evals/evals.json absent — covered by test_evals_shape")
    data = json.loads(_read(p))
    ids = [e["id"] for e in data["evals"]]
    assert any(i.startswith("pos-") for i in ids), f"I3 {skill}: no pos- case in evals"
    assert any(i.startswith("neg-") for i in ids), f"I3 {skill}: no neg- case in evals"
    assert any(i.startswith("edge-") for i in ids), f"I3 {skill}: no edge- case in evals"


# -----------------------------------------------------------------------------
# I4 — ANTI-HYPE README (bilingual Limitations sections required)
# -----------------------------------------------------------------------------

def test_invariant_4_anti_hype_readme():
    en = _read(ROOT / "README.md")
    zh = _read(ROOT / "README.zh-TW.md")
    assert "## Limitations" in en, "I4: README.md must contain '## Limitations' section"
    assert "## 限制" in zh, "I4: README.zh-TW.md must contain '## 限制' section"


# -----------------------------------------------------------------------------
# I5 — HONEST PROVENANCE (every ARS mention paired with a bracketed ref)
# -----------------------------------------------------------------------------

@pytest.mark.parametrize("skill", ALL_SKILLS)
def test_invariant_5_honest_provenance(skill):
    p = SKILLS_DIR / skill / "SKILL.md"
    for line_no, line in enumerate(_read(p).splitlines(), start=1):
        if "ARS" in line or "academic-research-skills" in line:
            assert "[" in line and "]" in line, (
                f"I5 {skill} SKILL.md:{line_no}: ARS mention without bracketed reference: {line!r}"
            )
