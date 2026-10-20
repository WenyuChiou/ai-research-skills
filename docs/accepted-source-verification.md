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
