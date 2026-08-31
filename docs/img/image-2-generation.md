# Image 2.0 flowchart generation record

Checked on: **2026-08-31**

This record covers the six flowcharts rendered in the English and Traditional
Chinese landing READMEs. It records an approved H3 external-generation run; it
does not authorize unrelated API experiments, scholarly live dogfood, or writes
to Zotero, Obsidian, or NotebookLM.

## Visual system

- OpenAI built-in Image 2.0 generation/editing path.
- White and soft-blue canvas, navy `#0B2742`, teal `#2DA89C`.
- Crisp vector-like lines, rounded cards, restrained shadows, high-contrast type.
- Shared icon language and spacing across pipeline, architecture, and HITL views.
- No warning palette, AI-brain imagery, watermark, or invented product claim.
- English and zh-TW pairs preserve the same composition, hierarchy, node count,
  and edge direction. Skill identifiers and schema names remain untranslated.

## Content and topology contracts

### Pipeline overview

The previous reviewed pipeline image and
[`pipeline-overview-prompt.md`](pipeline-overview-prompt.md) were supplied as the
content contract. The generated output had to preserve all eight stages, every
skill chip, the four cross-cutting tools, the `17 / 12 / 4` counts, and the repo
URL. Stage 2 retained five chips and Stage 7 retained `paper-review`.

### Harness architecture

The authoritative Mermaid topology remains:

```text
Researcher -> research-hub workflow runtime
  -> Role agents -> ResearchEvidencePacket -> Deterministic validator
  -> Human gate
Human gate -- accept -> Truth stores -> Release artifact
Human gate -- decline / revise -> research-hub workflow runtime
Private host adapter -> agent-collab policy + checkpoint -> runtime
```

The semantic nodes remain grouped as the semantic research layer. The private
host adapter and optional public policy layer stay visibly outside the
research-domain runtime.

### HITL state machine

The reviewed terminal semantics are:

```text
Awaiting decision -- cancel -> Cancelled
Awaiting decision -- decline -> Declined
Awaiting release -- decline -> Declined
Awaiting release -- accepted authorization -> Completed
Recovery -- retry exhausted -> Blocked
Recovery -- reconcile / resume -> Running
```

`Cancelled`, `Declined`, and `Blocked` never become success. `Completed` is only
reachable through accepted release authorization.

## H3 dogfood findings

The pipeline pair passed the initial operator check, but independent review later
found an orange count marker and a missing safety-bearing `only` / `只處理` in
the Antigravity captions. Those outputs were rejected and corrected before
shipping. The architecture pair passed its first reviewed generations.

The first two English HITL drafts incorrectly routed release authorization and
recovery edges. A topology-first regeneration fixed those edges but introduced
a separate `Awaiting release -- decline` destination error. Long-distance arrow
rerouting remained unreliable, so the final accepted edit used a semantically
equivalent terminal-card and edge-label swap while preserving the reviewed
geometry. The zh-TW asset was then localized from that accepted English image.

This is the practical failure-mode lesson from H3: generated diagrams require a
deterministic topology contract and human semantic review; visual polish alone
is not acceptance evidence.

## Reviewed assets

| Asset | Dimensions | SHA-256 |
|---|---:|---|
| `pipeline-overview.png` | 917×1716 | `e8242b3b717ac1d8dc96ac7c0f90dbca126618385da45d53fa490e68fe8701d2` |
| `pipeline-overview.zh-TW.png` | 917×1716 | `68f45b6c3cc4cb0be7fac35ba171d970ce30ff28adea9dc744410933a2eadf9c` |
| `harness-architecture.png` | 913×1722 | `d2393d728352e6d18e5c06292d488d09903a69554acb30ca53209ca12055eae3` |
| `harness-architecture.zh-TW.png` | 914×1721 | `c53415b4fa9fd7abfb836a19803642c4543df81c6ff113a3bdc6c507daf910c9` |
| `hitl-state-machine.png` | 1536×1024 | `0006206f850bae11cbd98bb423fd21379c29ca517a4d45e7912946545e6d3322` |
| `hitl-state-machine.zh-TW.png` | 1536×1024 | `58e2469ddabd02856409f08c23bcb95d52b7b4a8552221467654f4245d7f2281` |

The machine-readable copy is [`image-2-assets.sha256`](image-2-assets.sha256).

## Regeneration checklist

1. Revalidate the 17-skill catalog and stage mappings.
2. Use the current English image as the style reference and the Mermaid/content
   source as the topology reference.
3. Generate English first; reject any missing label, node, count, or edge.
4. Localize zh-TW from the accepted English composition. Reject Simplified
   Chinese, English-prose leakage, or topology drift.
5. View all six outputs at original resolution and at README width.
6. Run the bilingual topology, local-link, and asset-hash tests.
7. Update `image-2-assets.sha256` only after independent review.
