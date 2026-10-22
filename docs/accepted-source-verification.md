# Verify a reviewed local source

The default `scripts/check_upstream_contracts.py --source REPO=PATH ...` mode
continues to check source layout, manifest name/version and SKILL.md identity.
It does not establish that the source is the reviewed revision.

Add `--accepted-source` with the same five explicitly supplied clones to check
the immutable commit **and tree** recorded in
[upstream-contracts.json](../test-corpus/integration/upstream-contracts.json).
Detached exact revisions are supported. The checker does not clone, fetch,
checkout, install, call a model or change the clones. Git must support
`--no-lazy-fetch`; missing Git, missing objects or missing worktree metadata
remain `unavailable`, never accepted. A known identity/content mismatch is a
failure, even when the plugin version is still 0.5.4.

The bounded relevant set is the plugin manifest, each catalog SKILL.md and
the repository's explicit `shared_references` list (at most 32). Relevant staged,
unstaged or missing files fail. Direct comparisons with reviewed blobs also
detect changed content hidden by Git index flags. Text CRLF/LF representation
is equivalent; other content changes are not. Index/object inspection avoids
Git status/diff refreshes and never invokes configured clean/process filters.
Executable modes are compared on POSIX; Windows file-mode semantics are not
certified. Unlisted files and the entire
working tree are not certified. This is a local source diagnostic, not a
sandbox or authentication of where a clone was downloaded. Concurrent mutations
can invalidate a report; pause writers and retain the reported identities.

## Stage 1 and Stage 2 coverage

The Hub list follows actual reads in the accepted skills: shared
`research-protocol.md` and `source-claim-audit.md`; the gap dossier,
dead-end-history and contribution-typing references; the design helper's
Socratic prompts and design-brief template; and `docs/direction-review-contract.md`.
These carry literature-search scope, closest/contrary/versioned evidence, gap
importance/answerability/material/resource limits and human selection into
design. Checking their source identity prevents an incomplete local copy from
earning stronger verification. It does not execute or semantically validate
those scientific checks. The catalog does not duplicate Hub implementation.

## Keep historical and runtime claims separate

The Hub commit `7e046383` is a **reviewed snapshot, not an installation pin**.
Marketplace `source.ref` remains `master`. A newer local clone fails this exact
snapshot check until separately reviewed; do not replace the snapshot, its
`checked_on`, catalog `verified_on` dates or install refs to turn a failure green.
Reports repeat the historical snapshot date, not a new verification date.
The fixture's existing source-layout scope remains its historical statement;
the opt-in report separately labels its stronger, bounded check.

Neither mode verifies live models, installed host loading, runtime capability,
scientific quality or continuing validity. The existing
[runtime capability guidance](system-assessment.md#version-and-dependency-matrix)
requires probing the actual Hub callable/schema before claiming optional
source-audit support. A plugin version or a matching source file does not prove
that an installed wheel has those capabilities. No runtime probe is performed
by this checker; missing capability remains unavailable.

## Manifest-only cache metadata observations

The marketplace follows upstream branches, while the accepted snapshot above
remains historical. `test-corpus/integration/manifest-observations.json` records
**only** newer observed plugin manifests for cache-version alignment. Run:

```bash
python scripts/check_manifest_observations.py
```

An unchanged accepted version needs no observation. Every changed marketplace
version requires exactly one record matching canonical repository, plugin name,
version and branch ref, plus full commit/tree/manifest-blob identities and the
observed UTF-8 manifest text. Missing, duplicate, malformed, stale or mismatched
records fail closed, even when no sibling source clones are present. Synthetic
records in tests are not upstream evidence.

The offline validator binds recorded manifest bytes to their Git blob hash.
Commit/tree IDs are recorded provenance: it does **not** independently prove
commit-to-tree-to-path linkage or remote origin. A maintainer must verify that
linkage from the canonical source before adding a real observation. The Zotero
0.4.0 observation comes from commit `e390313c82e76856a525e87a0ae2d0281499e3ab`;
that is an unpublished source candidate, not a published release (latest checked
release v0.2.0). The Hub 0.5.6 observation comes from merged master commit
`01e796d3201349367ebc9297f1f2448a4d9851a3`. Neither record is a local-only
candidate substitution or an absent-sibling skip.

These observations never update accepted commits, trees, `checked_on`, human
verification dates, historical source tables or skill-content acceptance.
`--accepted-source` is intentionally unchanged: it first compares the accepted
manifest identity with the **current marketplace**, then checks source identity
and relevant content. After a cache version advances beyond the accepted
snapshot, this check fails even for the exact historical checkout. It is not a
way to certify the old baseline against changed current metadata. A matching
newer manifest can pass the default source-layout check but still cannot pass
`--accepted-source`; separate reviewed-source acceptance is required. Manifest
observations alone establish neither host installation, runtime behavior,
scientific quality nor release publication.
