# Audit-first design contract (the 5 invariants)

This document is the **machine-checkable** version of the "academic skills
you can audit in 30 minutes" claim. The same five invariants appear in
`templates/test_skill_integrity.template.py` as actual assertions; every
skill in the `audit-first-skills` bundle runs them via a single
parameterized pytest. If a skill cannot pass these five rules, it does
not ship.

If you maintain a fork or want to write your own audit-first skill, the
contract below is what you opt into.

---

## Invariant 1 — Audit budget

> A researcher should be able to read every skill end-to-end in 30 minutes.

```python
assert wc_lines("SKILL.md") <= 350
assert count_files("references/") <= 8
assert total_markdown_lines_recursive() <= 2000
```

**Why a number?** Because every prior project that promised "small" without
a number drifted past it. ARS's `references/` for one skill can be 20+
files; a fresh reader cannot audit the surface in an afternoon. The 350 /
8 / 2000 limits are deliberate — they are tight enough to force discipline
and loose enough to write real instructions.

**What breaks if you exceed:** the integrity test fails CI; the commit
cannot ship without either (a) tightening prose or (b) explicitly bumping
the budget in this document and re-running with reviewer sign-off. The
budget is not silently mutable.

---

## Invariant 2 — No declarative-only gates

> Every claimed check is an assertion, not an annotation.

```python
assert "ARS_" not in skill_md          # no opt-in env-flag gates
assert "if env.get(" not in skill_md
assert "[TODO]" not in any_shipped_md  # no unresolved promises in user-facing prose
```

**Case study (what this forbids):** ARS's `data_access_level` is, per ARS
own design doc, "a declarative annotation, not a runtime-enforced
permission system." The annotation exists, the CI lints that the
annotation is present, but the LLM at run time can ignore it. Audit-first
treats that as the wrong default: a check that isn't enforced shouldn't
imply that it is.

The lint forbids the patterns most commonly used to wire feature flags
(`ARS_*` env names, `if env.get(...)` runtime branches) and forbids
unresolved `[TODO]` markers in shipped text — a `[TODO]` in user-facing
prose is the prose equivalent of "this check is declared but not
enforced."

---

## Invariant 3 — Eval-bundled with mandatory mix

> Every skill ships behavioral evals, with the mandatory positive/negative/edge
> mix that catches both false-negatives and false-positives.

```python
evals = load("evals/evals.json")
assert len(evals["evals"]) >= 5

ids = [e["id"] for e in evals["evals"]]
assert any(i.startswith("pos-") for i in ids)
assert any(i.startswith("neg-") for i in ids)
assert any(i.startswith("edge-") for i in ids)
```

**Why each kind matters:**
- **`pos-`** confirms the skill fires the intended behavior on inputs that
  should trigger it.
- **`neg-`** is the harder test: confirms the skill does NOT fire on
  inputs that should NOT trigger it (no over-flagging). Skills tend to
  drift toward false-positive over time; the `neg-` case catches that.
- **`edge-`** exercises the ambiguous middle (PARTIAL, SOURCE_SILENT,
  anchored-but-suspicious). The vast majority of real-world cases live
  in this band.

**Authoring rules** for the fixtures themselves are in [`FIXTURE_AUTHORING.md`][fa]
(shipped inside the `skill-lint` skill). Read it before writing a new
fixture — the [v0.2 case study in that doc][fa-t2] explains how a
synthetic year `2099` can vacuously satisfy a conditional `must_not` and
cross-trip a check the eval didn't cover.

[fa]: https://github.com/WenyuChiou/audit-first-skills/blob/master/skills/skill-lint/references/FIXTURE_AUTHORING.md
[fa-t2]: https://github.com/WenyuChiou/audit-first-skills/blob/master/skills/skill-lint/references/FIXTURE_AUTHORING.md#worked-case-study--phase-t-fixture-t2

---

## Invariant 4 — Anti-hype README, bilingual

> The README is honest about what the skill is for AND what it isn't.

```python
en = read("README.md")
zh = read("README.zh-TW.md")
assert "## Limitations" in en
assert "## 限制" in zh
```

**Why bilingual is enforced:** the convention is set by
`academic-writing-skills` (the precedent skill in this marketplace). The
`## Limitations` / `## 限制` sections are required because **the lack of
honest limitations is a feature of AI-hype**, and the rule prevents the
common drift "we added a feature, why mention what it can't do".

What goes in Limitations: tested-by-N-researchers, domain bias, what the
skill is not a substitute for, known-unverified-claims.

---

## Invariant 5 — Honest provenance

> Every external project the skill borrows from is paired with a verifiable
> reference, on the same line, every time.

```python
for line in skill_md.splitlines():
    if "ARS" in line or "academic-research-skills" in line:
        assert ("[" in line and "]" in line), \
            f"ARS mention without provenance: {line!r}"
```

**Why this matters:** if you adapt an idea from ARS (or any other project),
the reader needs to be able to trace it. A bare `"borrowed from ARS"`
without a bracketed reference is the same anti-pattern as a citation
without a DOI — easy to say, hard to verify.

The bracket can be a markdown link, a footnote anchor, or a manual `[Lu
et al. 2026]` style reference — as long as the line carries enough
information to find the source.

---

## What the invariants do NOT cover

The contract is intentionally narrow. It does not promise:

- **Behavioral correctness on real-world inputs.** Layer-3 acceptance
  (running the skill against a real manuscript) is required before
  high-stakes use; the integrity test is necessary, not sufficient.
- **Cross-model robustness.** The skills are written and tested by Claude.
  Cross-model independent judge (Codex/Gemini as second opinion) is in
  the v0.3 backlog.
- **Corpus-scale evaluation.** Calibrated FNR/FPR gold sets are v0.3 work,
  not v0.1 promises.

The contract is what we can enforce automatically today. The honest
backlog is what the contract cannot enforce but the project still owes
its users.

---

## How to read this in 30 minutes

1. This document (`audit-first-design.md`) — 5 minutes.
2. [`why-not-ARS.md`](why-not-ARS.md) — 5 minutes.
3. One skill's `SKILL.md` of choice (≤350 lines) — 5 minutes.
4. That skill's `references/` (≤8 files, ≤200 lines each typical) — 10 minutes.
5. That skill's `evals/evals.json` and the 5 fixture files — 5 minutes.

If any of the five files in step 3–5 cause you to lose the thread, that's a
bug. Open an issue.
