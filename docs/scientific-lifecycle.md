# Scientific lifecycle and quality gates

The [pipeline](pipeline.md) remains the same eight-stage, researcher-led design.
This companion specifies what must be carried across its boundaries. A skill,
valid file, successful command, or green CI does not certify a scientific claim.
Use checks proportionate to the requested task; a quick lookup does not need a
whole-project audit. [System assessment](system-assessment.md) records current
coverage and verification limits.

繁中: [scientific-lifecycle.zh-TW.md](scientific-lifecycle.zh-TW.md)

## Stage inputs, outputs, and advancement

| Diagram stage | Inputs and existing route | Required handoff and quality evidence | Human decision or stop condition |
|---|---|---|---|
| 1. Discover literature | User question, inclusion constraints, unresolved information needs → research-hub/native search; Zotero for library operations | Need-to-query map; actual executed queries/search dates; work and version identity; inclusion/exclusion reasons; source access/evidence level; core, closest, classic, and contrary roles where relevant | Researcher owns scope. Suggested geography/date/method does not become an undeclared filter. Timeout, 429, paywall, or missing payload is unknown/failure, never zero-result evidence |
| 2. Compare and find the gap | Identified source set → literature-triage-matrix, NotebookLM verifier, gap-to-topic | Claim–source matrix; located evidence for consequential findings; closest prior-work comparison; negative/contrary evidence and dead-end history; separate openness, contribution/importance, and feasibility judgments; `topic_dossier.gaps.yml` with unresolved limits | Researcher/advisor chooses the topic. Missing literature does not prove novelty. A method-only comparator cannot replace topical evidence; lack of DOI alone does not invalidate a provenance-identified archival source |
| 3a. Frame the problem | Candidate dossier and human answers → research-design-helper | `design_brief.md`: question, estimand/expected mechanism, assumptions, identifiability, discriminating controls/baselines, validation plan, risk register; mark unanswered and placeholder segments | Researcher approves the question and intended contribution. Placeholders cannot gate real research; unidentifiable or unanswerable claims return to framing |
| 3b. Plan | Accepted brief plus actual data/resource knowledge → research-context-compressor / research-project-orienter | `project_manifest.yml`, `experiment_matrix.yml`, `data_dictionary.yml`; preserved `provenance.from_gap`; data access, ethics/consent when relevant, time/compute/cost bounds, analysis plan, failure criteria; preregistration when required or claimed | Researcher commits scope/resources. A manifest captures state; it does not supply a missing method or authorize an experiment |
| 4. Design and build | Accepted design intent plus project-specific model/method specification → primary researcher/agent; bounded mechanical leaves via multi-AI router | Source-controlled implementation, method assumptions, data transformations, tests of equations/algorithms, baseline/control fixtures; exact dependency and version records | Researcher approves consequential design changes. `design_brief.md` is design intent, not a complete implementation specification. Mechanical delegate results require independent diff and acceptance review |
| 5. Execute, calibrate, validate | Approved experiment/analysis plan and project tools; manifests preserve context | Reproducible commands, code/data/model hashes or version identifiers, parameters/prompts/seeds where applicable, repeated-run design, run/failure logs, outputs, sensitivity/uncertainty, held-out checks and verification vs empirical validation | Costly/long runs need experiment authorization. Failed runs remain in the record. Code tests do not establish empirical validity; missing required results block inference |
| 6. Visualize and interpret | Verified outputs → plotting scripts from bounded delegates; interpretation stays primary | Figure/table provenance; denominators, units, uncertainty, exclusions, effect estimates, condition/population boundaries; captions tied to exact plotted data; analysis report explaining alternatives and limits | Researcher owns substantive interpretation. Uncertainty or a non-significant test cannot silently become equality, absence, causation, or mechanism |
| 7. Outline, draft, review, revise | Design, analyses, sources, figures/tables → paper-memory-builder, academic-writing-skills, paper-review | `.paper/claims.yml` / `.paper/figures.yml` as declared authorities; evidence-linked extended outline; question→method→result→interpretation→contribution alignment; study-design adapters; review maturity appropriate to available evidence; accepted revisions propagated to affected sections and companions | Author approves scientific/semantic changes. A fluent paragraph or clear outline does not fill missing evidence; local edits do not imply whole-paper review |
| 8. Submission readiness, response, wrap-up | Exact active manuscript and companions → academic-writing-skills, paper-review, project context capture | Exact-candidate and cross-file checks; references/metadata/declarations; venue requirements supplied or verified; supplements/data/code access; review-response ledger and current-artifact verification; explicit blockers/waivers; final state/version preserved | Author decides readiness and separately authorizes actual submission/publication/sharing. Authorship, ethics, legal agreements, payments, and external upload retain their own gates. No automatic journal submission is provided |

## Cross-stage scientific integrity

- Preserve question, population, geography, time window, estimand, and explicit
  nonclaims from the researcher; distinguish accepted decisions from suggestions
- Separate identity, source access, exact quote binding, and semantic support.
  Metadata, abstract, generated summary, and located full text support different
  claims. Hashes prove byte binding, not authenticity or scientific adequacy
- Compare the same work/version. Keep preprints, revisions, corrections, and
  retractions distinguishable; retain discovery observations and decision
  reversals, and reopen dependent claims when their authority changes
- Keep supported, partial, contradicted, and unverifiable findings visible.
  Contradictions retain methods/populations/conditions; failed attempts to find
  counterevidence do not justify inventing opposition
- Report bounded completion: covered needs, executed paths, assessed claims,
  known access/identity limits, unresolved gaps, and whether to continue. A
  paper count or exhausted budget alone cannot imply comprehensive coverage
- Use field-appropriate designs: qualitative/theoretical/data papers do not
  inherit an experimental IMRAD or preregistration requirement automatically

## Existing source responsibilities

- [research-hub](https://github.com/WenyuChiou/research-hub) owns discovery,
  ingestion/audit receipts, source fetching, strict ResearchEvidencePacket,
  workflow state, human gates, and the 12 workspace skills
- [academic-writing-skills](https://github.com/WenyuChiou/academic-writing-skills)
  owns manuscript authority/lifecycle, design-aware integrity, exact-candidate
  audits, scientific review, revision, and release-readiness checks
- [zotero-skills](https://github.com/WenyuChiou/zotero-skills) owns deep library
  CRUD; library deduplication does not establish work/version claim identity
- Codex and Antigravity leaves do bounded mechanical work. Native/plugin
  loading, wrapper behavior, scientific validity, and publication authority are
  separate checks; see [runtime contract](runtime-contract.md)

## Verification and architecture boundary

These gates clarify the existing stage contracts; they add no stage, agent,
truth store, autonomous experiment runner, or journal-submission service. The
existing pipeline content contract, Mermaid architecture/state topology, and
reviewed image assets remain authoritative and unchanged. If a later change
alters a role, node, edge, or stage assignment, update its canonical source,
regenerate in the same visual design, and revalidate both locales and hashes.

Document/fixture consistency is structural evidence. Production validators and
native ingest previews provide behavior evidence at their specific boundaries.
An actual host-load check or research-quality comparison must be reported
separately, with its environment, inputs, failures, and unverified parts.
