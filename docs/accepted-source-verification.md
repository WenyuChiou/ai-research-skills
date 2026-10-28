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
failure, even when the plugin version is unchanged.

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

## Future native-reader source and handoff coverage

The fixture `test-corpus/integration/native-reader-future-contract.json` is an
authored synthetic consumer contract, **not current accepted-source verification**.
It does not advance the historical Hub commit/tree/date/version, marketplace
cache metadata or manifest-only observation. The catalog owns this acceptance
guidance; the upstream Hub owns its schema, renderer and skill content.

For a separately reviewed future native-reader source, retain all 12 SKILL files
and eight existing references, then cover these four additional exact paths:

- `skills/research-hub/references/native-discovery-export.md`
- `skills/research-hub/scripts/render_native_reader.py`
- `src/research_hub/schemas/research-discovery-observations-1.0.json`
- `skills/research-hub/references/research-discovery-observations-1.0.json`

That is 24 skill/dependency paths plus the plugin manifest: 25 checked files.
The existing checker can compare Markdown, Python and JSON bytes using an
explicit candidate reference list. Synthetic Git tests exercise missing files,
content changes hidden by index flags, and manifest drift without editing the
active accepted snapshot. Default layout success is weaker than source
acceptance. Matching cache metadata does not accept new skill content.
This bounded set is not the complete memory/summary dependency closure. It does
not cover the changed paper-memory claims schema, YAML schemas, revision-history
schema or Zotero summary-note ownership guidance; it cannot establish those
runtime contracts. Plugin source metadata is not a package release or proof of
an installed host. Verify actual candidate bytes and packaged mirrors separately.

A future actual renderer handoff must retain supplied raw hits, discovered,
screened, included, reading-depth counts and core count, including unknown totals
and the distinction between works and versions. Preserve overlapping roles,
reading/access limits and existing assessment decisions; do not infer inclusion
or invent summaries. In each supplied language entrypoint, expose the supplied
counts and discoverable links to the selected `assessment-status.sidecar.json`
and `README.md` when those are part of the delivery. Check required links as
well as whether links already present resolve; JSON existing elsewhere is not
discoverability. Preserve original work/version-bound statuses in the sidecar.

The small HTML/JSON fixtures test these consumer requirements with authored data;
they do not execute the Hub renderer, install a host, read a paper, authenticate
evidence, validate the upstream JSON schema or establish translation parity.
Actual candidate output inspection and exact reviewed-source acceptance remain
separate gates. No source-content acceptance is earned by these fixture passes.

## Keep historical and runtime claims separate

The bounded Hub source review dated 2026-10-28 records commit `4d83b8b`
(plugin source metadata 0.5.14), covering 12 skills, 12 shared references and
the manifest. Its provenance and the earlier 0.5.4 acceptance are preserved in
[Hub source history](../test-corpus/integration/hub-source-acceptance-history.json).
The shared `checked_on` remains the historical 2026-10-19 date; it is not a
new review date for the other repositories. Marketplace `source.ref` remains
`master`: the reviewed commit is not an installation pin. The 25-path check
does not cover the full memory/summary dependency closure, an installed host,
model execution or scientific end-to-end acceptance. Plugin metadata 0.5.14
is not a Python package release or an installed-host version.

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
release v0.2.0). The earlier Hub 0.5.10 observation is preserved in the Hub source history,
not the active list: the current marketplace and accepted Hub versions agree.
The 0.5.14 manifest bytes and Git identities are recorded in that history.
The validator still rejects extra records for an unchanged accepted version.

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
