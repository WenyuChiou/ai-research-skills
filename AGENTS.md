# Code Review Rules

This repository is a catalog index; skill content lives in upstream source
repositories. Keep the existing `CONTRIBUTING.md`; this file supplements it.
These rules apply only while conducting code review. They do not replace
implementation or publication instructions or valid authorization for other tasks.

- Review the actual diff at the stated base and head, then route by changed
  path: `catalog/skills.yml`, `.claude-plugin/marketplace.json`,
  `test-corpus/integration/upstream-contracts.json`, `docs/`, `scripts/`, or
  `tests/`. Read the relevant existing contract and its immediate producers and
  consumers; do not treat this catalog repo as the upstream skill source.
- For catalog and marketplace entries, bind source identity and version to the
  immutable commit or other exact identity required by the current contract.
  Check that catalog pins, marketplace source/ref, plugin manifest, and source
  layout agree; a floating name or current branch is not immutable evidence.
- For batch routing and cross-skill integration changes, follow the declared
  dependency graph and check producer/consumer artifact paths and formats
  together, including the applicable contract in
  `test-corpus/integration/upstream-contracts.json`. A fixture pass establishes
  only the behavior exercised by that fixture, not host loading or research
  quality.
- For installation and source-checking changes, inspect trusted-source
  constraints, dry-run behavior, argument quoting/escaping, and failure paths.
  A dry run or static manifest check does not establish a real host install.
- For Windows shell behavior, distinguish Git Bash from WSL; evidence from one
  environment must not be presented as validation of the other. The repository's
  current CI scope is Ubuntu; do not claim Windows CI coverage without an actual
  Windows run and its evidence.
- For generated or bilingual assets, compare the source and generated outputs
  for semantic parity and exact path/identity references. Keep offline checks
  distinct from live source access and live host behavior.
- For a bug fix, inspect representative tests for the failure and a safe
  case. Where feasible, check sensitivity using a known faulty baseline or a
  bounded negative case. Report missing case coverage separately from whether
  failure against old behavior is unverified; a green test alone does not prove
  the fix.
- For installation, version, or source-pin changes, compare the selected
  immutable source, manifest version, distributed payload, and relevant cache
  or loaded identity where evidence is available. If actual host loading was
  not checked, state that gap; do not describe an upstream draft as accepted.
- For changed first-use instructions, trace the documented path, prerequisites
  and failure recovery; flag unnecessary repeated work without removing needed
  safeguards or claiming user acceptance. For changed bounded handoffs,
  distinguish best-effort partial output from guaranteed delivery after a hard
  timeout or stuck call.

- Findings must identify a concrete path and line/symbol, trigger, consequence,
  and evidence. Separate confirmed defects, hypotheses, and verification gaps;
  omit style-only preferences and use the platform's required finding format.
- A review task itself does not modify code, install dependencies, start paid
  models, or merge. Every PR merge needs separate explicit user consent after
  the user receives the review summary, actual test status, and remaining gaps.
