# System assessment and staged integration

Checked against the public source revisions below on **2026-10-02**. This is an
AI-for-science lifecycle assessment, not evidence that an autonomous system has
completed a research project. The catalog remains a registry/routing layer;
production contracts live in the source repositories.

繁中: [system-assessment.zh-TW.md](system-assessment.zh-TW.md)

## Version and dependency matrix

| Source | Checked commit | Accepted package / plugin | Contract and verification boundary |
|---|---|---|---|
| ai-research-skills | [eee76f8](https://github.com/WenyuChiou/ai-research-skills/tree/eee76f87c3f4fbfe3cf6dcab865a657295985e01) | Catalog 1.7.2 / schema 4 | 17 skills, 5 source plugins; optional harness omitted by the legacy-v3 view; source directory and marketplace URL/ref must resolve the same SKILL.md |
| research-hub | [a643ace](https://github.com/WenyuChiou/research-hub/tree/a643aceefc52cbf690264a3801e597d787ebd714) | Python/MCP package 1.2.0 / research-workspace plugin 0.5.1 | 12 skills; native papers input, provenance/source_records, preview/idempotence; search audit/source fetch; strict ResearchEvidencePacket v1; workflow state and human gates |
| academic-writing-skills | [c28f0de](https://github.com/WenyuChiou/academic-writing-skills/tree/c28f0dedb312e9c99c0e8e15c37464f542471b43) | Plugin 1.2.0 | Scope-aware writing/review, design adapters, manuscript state, exact-candidate gate, cross-artifact changes and release blockers; no rewrite needed merely to claim integration |
| zotero-skills | [5b21974](https://github.com/WenyuChiou/zotero-skills/tree/5b219747358a16e068f54d139e408d00ddd755f0) | Plugin 0.3.0; latest checked tag 0.2.0 | Nested skill plus repository-root client; value-free credentials_status; CRUD/restore/merge/attach. Manifest/changelog version and actual release tag are different axes |
| codex-delegate | [438f92e](https://github.com/WenyuChiou/codex-delegate/tree/438f92e4cf9b0607b25109cebfc427d27d5e1942) | Plugin 0.1.0 | On-disk brief, wrapper status/result contract, primary acceptance review; advertised portable wrapper path absent in accepted source at assessment |
| antigravity-delegate | [a9c60d4](https://github.com/WenyuChiou/antigravity-delegate/tree/a9c60d4e40ddc06d0185ad041dcf0fb7bc398744) | Claude plugin 0.1.0 | Bounded mechanical lane; legacy CLI invocation. Current Google-native plugin surface is distinct from the Claude marketplace manifest |

The machine-readable public-source snapshot is
[upstream-contracts.json](../test-corpus/integration/upstream-contracts.json).
These accepted-source identities remain separate from proposed upstream changes.
Never update a stable marketplace claim to an unmerged preview branch merely
because its local tests pass. In particular, an open research-workspace proposal
is not an accepted execution contract.

Optional governance dependency: the catalog retains `agent-collab-harness`
0.4.0/v1. Current official release is
[0.5.1](https://github.com/WenyuChiou/agent-collab-skills/releases/tag/v0.5.1),
whose documented v1 interfaces remain compatible. Official 0.4.0/0.5.1 wheels
match their published hashes and each pass the exercised 22-check legacy hub
workflow-runtime suite. The [builder guide](for-agent-harness-builders.md)
preserves normal registry install plus a checksum-bound 0.4.0 release fallback;
registry failure here is environment-specific. No v2 migration or new trust
root is performed.

## Lifecycle coverage and remaining scientific gaps

The eight diagram stages already span literature, gap/topic choice, design,
planning, execution, interpretation, writing/review, and submission readiness.
[Scientific lifecycle and quality gates](scientific-lifecycle.md) makes their
inputs, outputs, evidence limits, and researcher decisions explicit.

Strong current coverage includes library/workspace operations, native discovery
handoff, source/audit receipts, topic/design dossiers, resumable state/gates,
and the writing/review evidence chain. Important boundaries remain:

- A retrieved list does not prove information-need coverage; a corpus omission
  does not prove an open or important gap
- Cheap screening is useful, but a famous remembered finding, DOI, abstract, or
  generated brief cannot be promoted to a full-text-supported central claim
- Source-byte/quote/version checks can reject mechanical inconsistencies;
  scientific support, novelty, importance and feasibility remain substantive
  judgments by the researcher with inspectable evidence
- Project manifests preserve state; they are not a domain-independent model
  builder, statistical-method selector, validation engine, or experiment runner
- Delegates can generate plotting/scaffolding; interpretation and research
  honesty remain primary. Submission readiness is not authorization to submit

## Minimal staged changes and dependencies

1. **Catalog hygiene and resolver acceptance.** Correct 15 repository-relative
   directories, synchronize accepted research-workspace 0.5.1, replace invalid
   whole-repo-to-single-skill installs, and label old Zotero shadowing evidence
   historical. Validate path/ref identity in deterministic CI and optionally
   inspect all five real source clones with the read-only checker. Installer
   dry runs are repeatable; invalid scopes/arguments and native failures stop
   before later commands
2. **Upstream plugin compatibility.** Repair installed-skill Codex wrapper
   packaging/brief resolution; assess verbose-output completion and versioned
   CLI claims in Antigravity. Native package markers need official-schema
   evidence and offline checks. These changes belong in their respective
   source PRs; current native-host execution remains separately unverified
3. **Shared research evidence discipline.** In research-hub, connect substantive
   information needs to executed native search paths; strengthen source-level,
   work/version, claim-binding and bounded-completion consumers. Reuse existing
   audit/source-fetch/native-input tools. Any optional evidence profile must be
   versioned alongside strict packet v1, not extra properties silently inserted
   into it. No AutoResearch ledger/operator or paid evaluation framework is
   transplanted
4. **Accepted integration.** Test actual producer/consumer fixtures and legacy
   contracts, review exact final diffs, run all required suites, then use draft
   PRs. Upstream changes must be accepted before a follow-up catalog version
   advertises them as stable. Merge, release, deployment, local installation,
   scientific submission and private-data upload retain separate authorization

## Comparable checks and limits

Catalog regression input is the same 17-skill public snapshot plus the same
installer invocations. Before fixes, seven install-contract cases failed:
wrong directories, invalid nested-repo install guidance, absent dry-run, and
four invalid-argument cases. They pass after the fixes. Additional tests reject
path traversal/ref drift/missing producers and preserve native failure status.
This establishes resolver and script behavior, not better literature research.

Source-repo behavior checks should invoke actual validators, wrappers, source
receipts or native ingest previews. Preserve legacy packet validity, provenance,
idempotent preview/replay, unknown/partial claims, version mismatch, unavailable
provider, and fabricated quote cases. Report structural checks, production
boundary tests, live host loading, and research-quality evaluation separately.

In this cloud assessment, Codex CLI help/version was inspectable; no live paid
model request was made. Claude and Antigravity executables were absent, so actual
marketplace/native-host loading remains unverified. Existing PowerShell Core
7.6.6 was found and exercised on Linux; native Windows behavior remains
unverified. Synthetic CLI doubles test wrapper behavior; they do not prove
real-host interoperation. Historical verification dates/tiers are not refreshed
by this source-layout audit. No scientific performance gain is claimed.

## Architecture and image decision

The existing English/Traditional Chinese pipeline, architecture and HITL PNGs
were inspected against their canonical prompt/Mermaid sources and hash
manifests. The proposed work strengthens existing contracts and the validator
boundary without changing stages, roles, stores, nodes or edges. Therefore the
original visual design/topology and reviewed images stay unchanged. The prose
cross-cutting table is corrected to include the orchestrator already shown in
the diagram. A later topology change must update canonical sources and all
reviewed exports in the original design, not introduce an unrelated diagram.
