## What this PR changes

<one or two sentences>

## Related upstream PRs (if any)

If this PR coordinates with a change in `WenyuChiou/research-hub`,
`academic-writing-skills`, `zotero-skills`, `codex-delegate`, or
`antigravity-delegate`, link the upstream PR(s) here. Per
[CONTRIBUTING.md](../CONTRIBUTING.md), source-dir renames and
artifact-contract changes need lockstep updates here.

- Upstream PR: <link, or "N/A">

## Checklist

- [ ] `python -m pytest tests/ -q` passes locally
- [ ] If a skill name / source dir changed: `catalog/skills.yml` +
      `.claude-plugin/marketplace.json` updated to match upstream
- [ ] If a SKILL.md URL changed: every doc referencing it
      (`README.md`, `README.zh-TW.md`, `docs/pipeline.md`,
      `docs/pipeline.zh-TW.md`,
      `docs/researcher-workflow-checklist.md`,
      `docs/skill-directory.md`, `catalog/skills.yml`) updated
- [ ] If user-facing wording changed in `README.md`: mirrored in
      `README.zh-TW.md`
- [ ] If workflow stages, mutation class, or a human gate changed: schema,
      fixtures, and report-only automation were rechecked
- [ ] Remote source manifest version/default ref and SKILL.md paths pass
      `python scripts/check_skill_health.py --strict`
- [ ] EN/zh-TW skill counts and pipeline/social visual counts still agree
- [ ] CONTRIBUTING.md updated if the catalog ↔ upstream contract
      changed

## Independent review gate

- Author self-check: <summary>
- Independent reviewer: <agent/report identity; must not be the author or implementer>
- Reviewed base SHA / head SHA: <full SHA> / <full SHA>
- Reviewed tree SHA and published-head match: <if reviewing a local snapshot>
- Verdict and findings: <pass, changes requested, or blocked; link evidence>
- Applicable tests and latest-head CI: <passed / failed / not run, with evidence>
- Remaining gaps/blockers: <list or none>

A formal GitHub `APPROVED` review is not required by this process. Any new
head needs a fresh independent review. Actual repository protections and
separate merge authorization still apply. Do not submit `APPROVE` solely to
satisfy this checklist. See [review governance](../docs/review-governance.md).

## Verification

How did you confirm this works end-to-end? (e.g.
`bash scripts/install-all.sh` + `claude plugin list` shows ✔ enabled
for the affected plugin)
