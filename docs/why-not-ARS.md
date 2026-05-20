# Why this marketplace is not ARS — and when to pick which

The reference point for academic skill suites in Claude Code is
[`Imbad0202/academic-research-skills`][ars] ("ARS"). It is a mature,
comprehensive academic pipeline plugin: ~v3.9.4 at time of writing,
~136 KB CHANGELOG, 200+ tests, 90+ `check_*.py` lints, a 10-stage
orchestrator that runs research → write → review → revise. Read the
[ARS README][ars-readme] to see the scope.

This marketplace does not try to be ARS. The skills under
`audit-first-skills` (and the `skill-lint` meta-skill) are deliberately
**the lean, audit-first alternative**.

[ars]: https://github.com/Imbad0202/academic-research-skills
[ars-readme]: https://github.com/Imbad0202/academic-research-skills#readme

---

## Decision matrix

| Pick ARS if you want… | Pick `audit-first-skills` if you want… |
|---|---|
| End-to-end pipeline orchestration (10 stages, RQ→ship) | À-la-carte per-skill use, no orchestrator |
| Maximal coverage of every honesty primitive (7-mode integrity, claim-faithfulness, contamination signals, calibration, repro_lock, …) | A small, opinionated subset of the highest-leverage ones |
| Active feature-flag toolkit (`ARS_CLAIM_AUDIT=1`, `ARS_PASSPORT_RESET=1`, …) you can opt into per stage | Every feature default-on; no opt-in flags by design |
| Comprehensive documentation set + showcase artifacts | A skill suite a researcher can audit in 30 minutes |
| To run as a one-stop autonomous pipeline | To spot-audit a manuscript section or a reference list |

ARS is the right pick when you want the full apparatus. `audit-first-skills`
is the right pick when you want to **read every skill end-to-end before
trusting it on your paper**, and you want the audit budget to be
machine-enforced — not aspirational.

---

## Comparison axes (verifiable, not hype)

| Axis | ARS (v3.9.4) | `audit-first-skills` (v0.1) |
|---|---|---|
| Install | `/plugin marketplace add Imbad0202/academic-research-skills` | `/plugin marketplace add WenyuChiou/ai-research-skills` |
| Skills shipped | 4 + orchestrator | 5 (no orchestrator) |
| Lines of CHANGELOG | ~136 KB | starts at ~1 KB; budget-capped |
| `check_*.py` lints | 90+ | 1 (`_selftest/lint_skill.sh`) |
| Schema versions | Schema 13.1 with `allOf` branch gymnastics | single eval format, no schema versioning |
| Opt-in env flags | multiple (`ARS_CLAIM_AUDIT`, …) | zero by design |
| Test infra | 200+ pytest with GH Actions CI | 1 `tests/test_skill_integrity.py`, parameterized across all skills |
| Public reference paper | yes (showcase PDFs) | none — clean synthetic exemplars only |
| Corpus-scale evaluation | declared as future work in ARS's own docs | also future work (v0.3 backlog) — disclosed honestly |
| Calibration gold-set FNR/FPR | 20-tuple gold set, default OFF | future work (v0.3) |
| Bias mitigation | cross-model verification (opt-in) | in-session author=judge with explicit bias-mitigation discipline; cross-model judge in v0.3 backlog |

The honest summary: **ARS is wider, this suite is narrower-and-thinner**. The
narrower is intentional — see the design contract in [`audit-first-design.md`](audit-first-design.md).

---

## What this marketplace deliberately does NOT offer

1. **No pipeline orchestrator.** No "stage 1 → stage 2 → integrity gate"
   chaining. Every skill is invoked individually by a human researcher.
2. **No opt-in feature flags.** Every check in every skill is default-on.
   If a feature ships, it ships ON.
3. **No declarative-only gates.** ARS's `data_access_level` is explicitly
   "a declarative annotation, not a runtime-enforced permission system" in
   its own docs. Every gate in this suite is either a real assertion (in
   the integrity test) or a human-readable rule the persona must follow.
4. **No release ceremony beyond what semver requires.** No "spec naming
   offsets", no schema-version branches.
5. **No claim of generality beyond the tested domain.** The skills lean
   water-resources / hydrology / agent-based modeling (the corpus they
   were distilled from). That bias is disclosed in every skill's README
   `## Limitations` section, not papered over.

---

## What ARS does that this suite intentionally does not (and that's fine)

- **The 7-mode AI research failure taxonomy (Lu et al. 2026).** This suite
  ports M1 / M3 / M5 (the modes most relevant to simulation papers) into
  `senior-author-review`'s Result-Integrity Pass, but does not implement
  the full 7-mode pipeline gate. If you want all 7 modes blocking your
  pipeline at Stage 2.5, use ARS.
- **Claim-faithfulness with retrieved-source audit.** ARS's L3 audit
  retrieves the cited source and judges whether the claim is supported.
  `verify-references` does the same at the prompt level (Step 6) but does
  not ship the L3 retrieval infrastructure. If you need automated
  per-citation source retrieval at corpus scale, ARS has that infrastructure.
- **Material Passport + repro_lock + Sprint Contract**. None of these are
  in scope here. ARS uses them; this suite trades them for the 30-minute
  audit promise.

---

## Honest caveats

- This marketplace is maintained by one graduate-student researcher.
  Tested over hours, not at corpus scale.
- The `senior-author-review` persona was generalized from a real
  water-resources / ABM research group; the style rules retain that
  lineage. Useful for similar papers; not yet validated for social
  sciences / ML / clinical writing.
- No claim to replace ARS. Explicit positioning: **the lean alternative,
  not the comprehensive one**.

For the design contract that makes the "audit in 30 minutes" promise
machine-checkable, see [`audit-first-design.md`](audit-first-design.md).
