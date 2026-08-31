# Human-in-the-Loop Research Workflow Delivery Plan

**Objective:** Audit the catalog and its sources, remove or replace unusable
skills, add a resumable end-to-end research control plane, and ship a workflow
that advances safe work automatically while preserving explicit human decisions
for consequential actions.

**Release shape:** 17 active skills, 5 installable Claude plugins, 5 active
source repositories, 8 research stages, and one report-only monthly health
workflow. The catalog remains a registry and documentation repository; runtime
skill logic stays in each canonical source repository.

## Baseline evidence

- Catalog baseline: 35 tests passed and 1 failed because the academic-writing
  marketplace pin was 1.1.1 while its source manifest was 1.1.6.
- Source baselines: research-hub 131 passed / 1 skipped; academic writing 12
  passed; Zotero 59 passed / 1 skipped; Codex delegate 19 passed.
- The Gemini delegate wrapper suite had 2 passes / 6 failures. A local repair
  reached 20 passes and independent review approval, but the GitHub repository
  is archived and rejects pushes. It is therefore evidence for retirement, not
  an active deliverable.
- A 90-day audit found 16 drift items. All then-catalogued URLs were reachable,
  but scheduled CI could not detect remote manifest version drift.
- Pipeline and social images showed 15 skills while the catalog had 16, and the
  pipeline omitted `paper-review`.

## Decisions

1. Drop archived `gemini-delegate` from active installation and routing.
2. Replace its bounded mechanical lane with `antigravity-delegate`; keep CJK,
   long-context synthesis, research judgment, governance, and final review with
   the primary model.
3. Keep `.research/workflow_state.yml` as the resumable state record. Every
   action records scope, hashes, attempts, validation, provenance, and any human
   decision.
4. Automatically allow only read-only, deterministic, previewed, or reversible
   work within approved scope.
5. Require a scoped human gate before external writes, costly experiments,
   semantic manuscript changes, release/merge/submission, destructive cleanup,
   or research-scope commitment.
6. Treat MCP as capability-negotiated. Structured elicitation may collect only
   bounded decisions; secrets remain in host-managed authentication. Chat/CLI is
   the fallback when structured input is unavailable.
7. Scheduled automation is report-only. It may fetch public metadata, upload an
   immutable report, and reconcile one labeled issue. It never installs,
   edits, opens a repair PR, merges, publishes, or deletes.

## Delivery tracks

### A. Make the replacement delegate installable

Repository: `WenyuChiou/antigravity-delegate`

- Add `.claude-plugin/plugin.json` and the standard
  `skills/antigravity-delegate/` layout.
- Package `scripts/run_agy.sh` beside the installed skill, preserve mode 100755,
  and require byte parity with the root canonical wrapper.
- Validate the skill, plugin manifest, wrapper layout, and regression test.
- Independent review is required before merge.

Delivered by [antigravity-delegate PR #1](https://github.com/WenyuChiou/antigravity-delegate/pull/1).

### B. Add the research workflow orchestrator

Repository: `WenyuChiou/research-hub`

- Add `research-workflow-orchestrator` in source and installer mirror form.
- Cover orient, scope, discover, synthesize, design, execute, write, and release.
- Define state with structured pending actions, accept/decline/cancel decisions,
  bounded retries, recovery blockers, terminal invariants, and provenance.
- Require accepted `release_authorization` before a completed state.
- Replace archived Gemini routing with bounded Codex/Antigravity result
  contracts and fail-closed fallbacks.
- Validate JSON Schema behavior, source/mirror parity, installer discovery, and
  plugin/version inventory.

Delivered by [research-hub PR #128](https://github.com/WenyuChiou/research-hub/pull/128).

### C. Make the catalog machine-auditable

Repository: `WenyuChiou/ai-research-skills`

- Upgrade to catalog schema v4 with per-skill lifecycle metadata and an
  `extensions[]` surface; preserve a deterministic v3 compatibility view.
- Pin the current upstream plugin versions and require all 17 skills to be
  active, reachable, and represented in bilingual directory/pipeline docs.
- Fetch every active source repository's public metadata and plugin manifest;
  compare archived state, default ref, manifest name/version, skill path, and
  frontmatter identity.
- Parse only the first YAML frontmatter block so body text cannot spoof a skill
  identity.
- Add fixture tests for remote version drift, missing manifests, frontmatter
  boundaries, schema-version rejection, and checker-crash recovery.

### D. Close the report-only human loop

- Run monthly and on manual dispatch with read-only contents and issue-write
  permissions.
- Pin GitHub Actions by commit SHA and PyYAML by exact version.
- Always emit health, drift, and exit-code artifacts, including checker crashes.
- Reconcile only the exact `[skill-health] Human review required` issue under the
  `skill-health` label, include the run URL, reopen on recurrence, and close on a
  verified recovery.
- Preserve a human maintainer as the only actor authorized to choose and apply a
  repair.

### E. Synchronize bilingual docs and visuals

- Show 17 total skills: 12 in research-workspace and 5 skills across 4
  standalone source repositories.
- Include `paper-review` and `research-workflow-orchestrator` in English and
  Traditional Chinese pipeline art.
- Update the social preview, canonical prompt, dimensions, installation links,
  tier counts, and active delegate references.
- Preserve clearly labeled historical verification records rather than
  rewriting old evidence.

## Release gate

1. Merge upstream Antigravity and research-hub PRs before running the catalog's
   live health smoke.
2. Run the catalog pytest suite, schema and marketplace checks, workflow YAML
   parse, live remote health smoke, and plugin installation smoke.
3. Run independent code review on the final stable catalog diff; address every
   critical finding and perform targeted re-review.
4. Stage explicit paths and assert the exact staged-file count.
5. Push a catalog PR, wait for GitHub CI, squash-merge, delete feature branches,
   prune worktrees/remotes, and verify clean synchronized default branches.

## Acceptance criteria

- Antigravity, research-hub, and catalog PRs are merged; no task branches or
  extra worktrees remain.
- Catalog, marketplace, bilingual docs, prompts, and images agree on 17 skills.
- The live health report passes against all 5 active source repositories.
- Every consequential transition has accept/decline/cancel semantics and can
  resume without replaying an already validated external or costly action.
- Checker failure still produces an artifact and a durable human-review issue.
- Archived Gemini is absent from active installation/routing but remains in
  explicitly labeled historical audit evidence.
- Independent reviews have no unresolved critical findings and GitHub CI is
  green before each merge.
