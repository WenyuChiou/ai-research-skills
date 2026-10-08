# System assessment and staged integration

Checked against the public source revisions below on **2026-10-03**. This is an
AI-for-science lifecycle assessment, not evidence that an autonomous system has
completed a research project. The catalog remains a registry/routing layer;
production contracts live in the source repositories.

The academic-writing-skills row and snapshot were refreshed to the reviewed
1.3.7 release on 2026-10-07. The zotero-skills row and snapshot were refreshed
to the reviewed 0.3.1 release on 2026-10-07. Other source identities retain
the assessment above.

繁中: [system-assessment.zh-TW.md](system-assessment.zh-TW.md)

## Version and dependency matrix

| Source | Checked commit | Accepted package / plugin | Contract and verification boundary |
|---|---|---|---|
| ai-research-skills | [eee76f8](https://github.com/WenyuChiou/ai-research-skills/tree/eee76f87c3f4fbfe3cf6dcab865a657295985e01) | Catalog 1.7.2 / schema 4 | 17 skills, 5 source plugins; optional harness omitted by the legacy-v3 view; source directory and marketplace URL/ref must resolve the same SKILL.md |
| research-hub | [7e04638](https://github.com/WenyuChiou/research-hub/tree/7e046383368d85acb8dfbf0d734ecaaae335cf0a) | Python/MCP package 1.2.0 / research-workspace plugin 0.5.4 | 12 skills; native input/provenance/preview; optional source-audit and offline direction-review contracts; explicit human topic choice; strict packet v1 unchanged; installed runtime must be probed |
| academic-writing-skills | [061d73e](https://github.com/WenyuChiou/academic-writing-skills/tree/061d73ea4014e0486c2c753dbe9602dd9c3bb8ef) | Plugin 1.3.7 | Scope-aware writing/review, contextual sentence-frame/connector diagnostics, and first-draft handoff checks; optional coverage/hash validation is not editorial or scientific certification; no live host update is established here |
| zotero-skills | [f5772f8](https://github.com/WenyuChiou/zotero-skills/tree/f5772f8b62410858d41436efe11e85529b5dee8c) | Plugin 0.3.1; latest checked tag 0.2.0 | Nested skill plus root client; attach_pdf now sends a bare filename via upload_attachments(basedir=...), fixing an HTTP 400 that failed every 0.3.0 call; runtime and destructive safeguards unchanged |
| codex-delegate | [30f6d4a](https://github.com/WenyuChiou/codex-delegate/tree/30f6d4ae63935f5b71bd38d4d13466fcff5f33d8) | Plugin 0.1.1 | Bundled Bash/PowerShell wrappers; stable brief/result/sentinel adapter; dirty-content observation and sandbox forwarding; independent supervisor acceptance, not a second broker |
| antigravity-delegate | [c3afa59](https://github.com/WenyuChiou/antigravity-delegate/tree/c3afa59263ea02e40df99097ba5a9c4452e887a8) | Claude plugin 0.1.1 | Bounded mechanical lane; capped-log producer completion; minimal Google-native marker distinct from the Claude manifest; live native-host loading unverified |

The machine-readable public-source snapshot is
[upstream-contracts.json](../test-corpus/integration/upstream-contracts.json).
The catalog row records its accepted baseline; the other source rows now include
the reviewed source merges. Source acceptance does not publish a Python wheel.
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

Accepted [agent-collab source 4aa56e4](https://github.com/WenyuChiou/agent-collab-skills/tree/4aa56e47011b15a416f128b5a1c395baae8d0581)
adds task/run/baseline/current-candidate evidence review and makes mtime advisory.
Its presets are declarative review contracts, not a Python runtime preset
engine; this source-doc change does not modify either released wheel.

Research-workspace 0.5.4 retains the optional source-audit profile in accepted
source, while Python package version remains 1.2.0. A plugin update does not
replace an installed wheel. Probe `validate_evidence_packet` for `source_audit`
and `artifact_root` kwargs plus packaged `research-source-audit-1.0.json`, as in
the [installed-runtime instructions](https://github.com/WenyuChiou/research-hub/blob/7e046383368d85acb8dfbf0d734ecaaae335cf0a/skills/research-hub/references/source-claim-audit.md#optional-executable-source-audit-profile).
Missing capability remains unavailable for mechanical audit; retain manual/native
source review instead of calling unsupported kwargs or relabeling packet-only
validity. Do not infer that capability from the unchanged version string.

The accepted [direction-review contract](https://github.com/WenyuChiou/research-hub/blob/7e046383368d85acb8dfbf0d734ecaaae335cf0a/docs/direction-review-contract.md)
adds optional offline `paper direction-check` over supplied records:

- Bind `candidate_version` and `candidate_sha256` to the complete candidate,
  and evidence to actual source bytes. Preserve material-level provenance;
  a local note is not original full text. Publication version is recorded,
  not authenticated; explicit unknown remains unknown. Changed candidate
  content/version or source bytes require rechecking, retaining the old record
- Cover data/tool/model/license/cost/premise/validation-path with explicit
  supported/contradicted/unknown/not-applicable assessments. Unknown needs a
  bounded next check; justified not-applicable remains valid for theoretical work
- Sum declared resource components across the reviewed candidate scope; shared
  work needs explicit `sharing_basis`. No unit conversion occurs. Missing
  required units, demand or capacity remain unknown. Stale bindings invalidate
  current resource conclusions; supplied arithmetic is only diagnostic
- `semantic_assessment: not-performed`, `runtime_budget_verification: not-performed`,
  `human_selection: outside-checker`, `execution_authorized: false`. Exit 0 can
  include unknowns, contradictions or over-budget estimates. It is not research
  approval. The checker reads no Hub configuration, calls no model/network,
  writes no files and starts no next stage

The ordinary dossier and standalone design dialogue still work without the
optional review. A sole eligible candidate does not authorize pre-filling a
design brief: use the human's clear prior selection, otherwise ask. Preserve
human edits and ask before replacing provenance. Guidance now records prospective
outcomes/time boundaries, two-occasion and vignette claim limits, an applicable
matched-information comparison, minimum worthwhile gain and the smallest
answerable version with nonclaims; no fixed one-week prototype establishes
feasibility. These are source contracts, not a new quality finding: one guidance
comparison pair was inconclusive, and historical T1 dates/tiers remain unchanged.
No overall scientific improvement is claimed. Plugin 0.5.4 does not establish
that an installed Python wheel exposes this command; inspect its actual CLI
capability before use and keep the ordinary/manual path if unavailable.

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
   directories, align marketplace versions with accepted manifests, replace invalid
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
   PRs. The accepted source commits above now support the synchronized plugin
   versions and snapshot; an unmerged preview still cannot replace them.
   Merge, release, deployment, local installation,
   scientific submission and private-data upload retain separate authorization

## Comparable checks and limits

Before the first live model-backed test, use the
[preflight contract](live-run-preflight.md). Resolve effective host/provider/model,
subscription-versus-API mode, approved budget and data destination/scope; reuse
valid explicit choices and ask missing or materially changed choices before
calling a model. Its fixtures specify supervisor behavior, not runtime enforcement.

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

For normal Claude Code integration, prefer the [official codex-plugin-cc](https://github.com/openai/codex-plugin-cc/tree/db52e28f4d9ded852ab3942cea316258ae4ef346)
when its runtime fits. Keep codex-delegate for the existing synchronous brief,
sidecar/sentinel and Bash/PowerShell adapter contract, not another broker.
In one matched protocol fixture with `commandExecution` but no `fileChange`,
the official event-derived touched-file list is empty while the wrapper's Git
observation reports the actual edit; all adapters produce the same correct
artifact. This is conditional observation coverage, not evidence that real
shell edits always omit events or that the wrapper improves coding quality or
total model cost. Neither path enforces brief scope by itself.

Codex CLI help/version and actual PowerShell Core 7.6.6 on Linux were inspected;
new-head hosted Windows/Linux process fixtures pass. Claude and Antigravity
executables were absent, so marketplace/native-host loading remains unverified.
There is no successful matched live model quality/cost A/B. Synthetic delegates
test transport behavior, not real-host interoperation or sandbox certification.
Historical verification dates/tiers are not refreshed by this source-layout
audit. No scientific performance gain is claimed.

## Architecture and image decision

The existing English/Traditional Chinese pipeline, architecture and HITL PNGs
were inspected against their canonical prompt/Mermaid sources and hash
manifests. The proposed work strengthens existing contracts and the validator
boundary without changing stages, roles, stores, nodes or edges. Therefore the
original visual design/topology and reviewed images stay unchanged. The prose
cross-cutting table is corrected to include the orchestrator already shown in
the diagram. A later topology change must update canonical sources and all
reviewed exports in the original design, not introduce an unrelated diagram.
