# Round 2 H3 dogfood and failure benchmark

Run date: 2026-08-31

Environment: Windows 10, PowerShell 7.6.4, Python 3.14

Scope: live read-only scholarly discovery plus isolated local workflow recovery

Cost: USD 0; no paid API and no canonical Zotero, Obsidian, or NotebookLM write

This is a small failure-oriented dogfood report, not a general ranking or a
claim of statistical superiority. Phase 0 did not capture equivalent live
runtime metrics, so unavailable baseline cells remain **N/A** rather than being
reconstructed after the fact.

## Decision and safety boundary

H3 was explicitly approved for the three planned tasks. Live scholarly calls
were read-only. The interruption scenario used an isolated `.research`
directory and a declared no-write action. NotebookLM authentication had expired,
so its live check is **degraded/SKIP**, not PASS. No external mutation was
attempted.

## Three real tasks

| Task | Exact operation | Result | Duration |
|---|---|---|---:|
| Scoped discovery | `research-hub search "human-in-the-loop AI agents scientific research evidence verification" --limit 8 --field cs --rank-by smart --verify --json` | 8 results; Semantic Scholar returned HTTP 429 and the run degraded to other backends; one cross-backend DOI/arXiv duplicate exposed a real defect | 12.82 s |
| Contradictory evidence | Search `large language models simulate human survey responses validity bias`, verify three identifiers, then no-tool packet synthesis | 3/3 source identities verified; 3 supported claims; 1 contradiction and 1 evidence gap preserved; 0 unsupported claims accepted | 18.15 s |
| Interrupted workflow | Initialize an isolated workflow, inject interruption after a declared no-write action, resume, reconcile, resume again, retry the same action | Unknown outcome blocked with `reconcile_required`; explicit reconciliation resumed successfully; duplicate retry was rejected | 2.65 s |

The first interrupted-workflow attempt used the wrong operator-supplied state
filename and failed visibly. The corrected run used the CLI's actual
`.research/workflow_state.yml` contract. This operator error is retained as
evidence rather than omitted from the result.

## Before and after

| Observable | Phase 0 baseline | Round 1 + H3 observation |
|---|---:|---:|
| Offline research-hub suite | 3,321 passed; 3 failed; 23 skipped; 11 deselected; 2 xfailed | 3,348 passed; 0 failed; 23 skipped; 11 deselected; 2 xfailed |
| Live source identities verified | N/A | 3/3 |
| Unsupported live claims accepted | N/A | 0/3 |
| Contradictions preserved | N/A | 1/1 observed contradiction |
| Corrected interruption scenarios resumed | No executable workflow runtime | 1/1 |
| Duplicate no-write retries rejected | No workflow-wide action ledger | 1/1 |
| Replay failure invariants | No unified corpus | 12/12 PASS |
| Targeted timeout/recovery tests | N/A | 4 passed; 1 deselected |
| Paid provider cost | N/A | USD 0 |

The live sample is deliberately small. Counts describe this run only; they are
regression anchors, not estimates of field-wide accuracy.

## Failure injections and honest degradation

The recorded replay corpus passed 12/12 invariants: DOI conflict, unsupported
citation, contradictory papers, provider unavailability, prompt injection,
human decline, human revise, cancellation/resume, crash after external write,
duplicate retry, policy exhaustion, and unsupported NotebookLM claims.

Observed live failures:

- Semantic Scholar rate-limited both searches with HTTP 429. Other backends
  continued, and the provider remained visibly degraded.
- NotebookLM authentication was expired. The live provider check was skipped;
  only the recorded offline invariant passed.
- Cross-backend identity reconciliation treated one paper as two records when
  the arXiv backend supplied only an arXiv ID and another backend supplied both
  DOI and arXiv ID.

## Evidence-driven refinement

Only the demonstrated identity defect changed production behavior. The
research-hub refinement merges DOI and arXiv aliases transitively while
preserving first-backend title/abstract precedence and combined provenance.
Targeted tests passed 22 cases with 1 deselected; the complete local suite passed
3,348 tests. See [research-hub PR 130](https://github.com/WenyuChiou/research-hub/pull/130).

No new orchestration abstraction was added from aesthetic preference. Provider
429 handling and expired NotebookLM authentication remain explicit operational
conditions rather than being converted into false success.

## Reproduction and acceptance

Offline replay:

```text
python scripts/run_harness_replay.py
# 12/12 PASS
```

Research-hub verification on the refinement commit:

```text
python -m pytest tests/test_search_confidence.py -q
# 22 passed, 1 deselected

python -m pytest -q
# 3348 passed, 23 skipped, 11 deselected, 2 xfailed
```

Acceptance requires the public PR CI to be green. A live provider outage can
produce degraded/SKIP evidence, but it cannot be reported as PASS.
