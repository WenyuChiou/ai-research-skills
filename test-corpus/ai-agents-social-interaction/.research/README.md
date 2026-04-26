# `.research/` verification artifacts

These 8 files are the **outputs that the research-hub skills actually
produced** when run against the parent `ai-research-skills` repo on
2026-04-25. They are kept here as **reproducible evidence** for the
verification report at [`docs/verification.md`](../../../docs/verification.md).

This catalog repo is **not** a research project itself. The files below
were generated *as a test* of the catalogued skills, then relocated from
the repo root into this test-corpus subdirectory so the repo stays
clean for external users who clone it.

## File-by-file provenance

| File | Skill that produced it | Original location |
|---|---|---|
| `literature_matrix.md` | `literature-triage-matrix` | repo root → `.research/literature_matrix.md` |
| `project_manifest.yml` | `research-context-compressor` | repo root → `.research/project_manifest.yml` |
| `experiment_matrix.yml` | `research-context-compressor` | repo root → `.research/experiment_matrix.yml` |
| `data_dictionary.yml` | `research-context-compressor` | repo root → `.research/data_dictionary.yml` |
| `run_log.md` | `research-context-compressor` | repo root → `.research/run_log.md` |
| `open_questions.md` | `research-context-compressor` | repo root → `.research/open_questions.md` |
| `orientation_memo.md` | `research-project-orienter` | repo root → `.research/orientation_memo.md` |
| `multi-ai-routing-decision.md` | `research-hub-multi-ai` | repo root → `.research/multi-ai-routing-decision.md` |

## Path references inside these files

Paths inside these manifests (e.g., `entrypoints.primary_readme:
README.md`, `outputs: .research/literature_matrix.md`) are written **as
they were when the skill ran**, with the repo root as the working
directory. Those references are now slightly stale — the actual files
live one directory level deeper than the manifests imply. We kept them
verbatim because the value of these artifacts is "this is what the
skill *actually* produced", not "this is what we wish it had produced
after editing".

If you re-run any of these skills against your own research repo,
their natural output location will be `<your-repo>/.research/`, not
nested under `test-corpus/`.

## Re-running the verification

See the **Re-running the verification** section in
[`docs/verification.md`](../../../docs/verification.md) for the exact
command sequence.
