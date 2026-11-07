# Review governance and branch maintenance

[繁體中文](review-governance.zh-TW.md)

## Independent review gate

For this catalog repository, a passing independent subagent review satisfies
the review gate. A formal GitHub reviewer `APPROVED` submission is not required
by this process. Independence means a separate reviewing agent that neither
authored nor implemented the changes being reviewed, not the author relabeling
its self-check as review. A GitHub review may still provide useful findings.

Before marking a PR ready or merging:

1. Complete the author's self-check.
2. Have an independent subagent inspect the actual diff and relevant contracts.
   Record its identity/report, full base and head SHAs, scope, verdict,
   actionable findings, test evidence and verification gaps in the PR body or
   a linked report. A pass must have no unresolved blocking finding.
   If review uses a local snapshot, record its tree SHA and verify that the
   published head has the identical tree before reusing that review evidence.
3. Run applicable local tests and require necessary CI on the latest head.
   For this repository, run `python -m pytest tests/ -q`,
   `python scripts/check_marketplace_consistency.py` and
   `python scripts/check_catalog_schema.py`. Source/version changes also need
   the existing strict live source-health checks in `CONTRIBUTING.md`.
4. Recheck mergeability, unresolved review findings, current base and head.
   Any head change requires fresh independent review and affected tests/CI.
   If the base changes, review the integration diff and rerun affected checks;
   do not reuse evidence for an incompatible base.
5. Keep publication and merge authorization separate. The existing `AGENTS.md`
   requirement for explicit user merge consent after the review/test summary
   remains in force unless a current explicit user instruction covers the
   action. Passing review alone is not permission to merge, publish, release,
   deploy or delete branches.

Do not submit `APPROVE` to manufacture approval evidence. Do not waive known
blockers, failed required checks or real GitHub branch protections. If GitHub
requires a formal reviewer approval despite this process, report the exact
conflict for a separately authorized settings decision. This document does
not change rulesets, branch protection, permissions or repository settings.

## Configurable cleanup preview

The catalog has merged topic branches that can outlive their PRs. The planner
replaces manually checking each branch's PR status with one read-only report:

```bash
python scripts/plan_branch_cleanup.py
python scripts/plan_branch_cleanup.py --config /path/to/branch-cleanup.json
```

Prerequisites: Python 3.10+ and an already configured GitHub CLI (`gh`) with
read access to the repository. It uses only GitHub GET requests, paginates all
branches and PRs, and fails without producing a plan if metadata is incomplete
or a request fails. It does not sign in, create credentials, install anything,
change permissions or settings, or execute deletion. There is no `--apply`.

`.github/branch-cleanup.json` contains these defaults:

| Setting | Default | Meaning |
| --- | --- | --- |
| `repository` | `WenyuChiou/ai-research-skills` | Exact repository to inspect |
| `allowed_prefixes` | `codex/`, `docs/` | Literal topic-branch prefixes; each ends in `/` |
| `allowed_pr_authors` | `WenyuChiou` | Only merged PRs by these authors can be candidates |
| `keep_patterns` | `main`, `master`, `release/*`, `keep/*` | Case-sensitive shell-style patterns to retain |
| `minimum_age_days` | `7` | Minimum full elapsed days since merge |

An empty prefix or author list disables candidates. Keep patterns take
precedence. The default branch and protected/unknown-protection branches are
always retained, even if a customized allowlist includes them.

A candidate needs a merged PR into this repository's current default branch,
from this same repository, with the **exact current branch head SHA** and an
allowed PR author. The planner retains branches with an open PR, an open PR
that depends on them as its base, a closed unmerged PR, unknown source identity,
no matching merged PR, changed heads or insufficient retention. A squash-merged
PR is supported through its recorded head SHA rather than Git ancestry alone.
Fork branches are never cleanup targets; orphan or unmerged branches are not
inferred safe from their age. Author allowlisting does not prove sole branch
ownership or absence of other contributors' work.

Every result is `report-only` with `deletion_authorized: false`. A candidate
is not a deletion instruction. Before separately authorized cleanup, refresh
the remote head and protections, recheck all PR dependencies, confirm that no
contributor or active task still uses the branch, check local worktrees, and
record the exact repository/branch/SHA and merged PR for recovery. If the ref
has moved or anything is uncertain, retain it. Never delete another person's
work, an in-use branch, an orphan/unmerged branch or the default branch through
this maintenance process. This planner does not schedule automatic cleanup.

## Offline verification and limits

`--snapshot /path/to/snapshot.json` reads a complete offline export with keys
`repository`, `branches`, `pulls`, `complete: true`, and `captured_at` (an ISO
timestamp with timezone). The first three contain the GitHub REST repository
object and fully paginated branch/PR arrays. Snapshots must be at most 24 hours
old and are input evidence, not proof that the remote state still matches.
Use only trusted exports; the completeness marker is an assertion, not an
independent pagination audit. Do not store private exports in this public repo.

Run `python -m pytest tests/test_branch_cleanup.py -q` for offline filtering,
pagination, failure and no-mutation coverage. Unit fixtures are not live GitHub
or deletion tests. Live reports remain point-in-time previews and cannot detect
other computers' worktrees or unpushed changes. No branch deletion is tested or
performed by this tool.
