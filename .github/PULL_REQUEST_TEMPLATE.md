## What this PR changes

<one or two sentences>

## Related upstream PRs (if any)

If this PR coordinates with a change in `WenyuChiou/research-hub`,
`academic-writing-skills`, `zotero-skills`, `codex-delegate`, or
`gemini-delegate-skill`, link the upstream PR(s) here. Per
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
- [ ] CONTRIBUTING.md updated if the catalog ↔ upstream contract
      changed

## Verification

How did you confirm this works end-to-end? (e.g.
`bash scripts/install-all.sh` + `claude plugin list` shows ✔ enabled
for the affected plugin)
