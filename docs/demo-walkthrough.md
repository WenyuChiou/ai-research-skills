# Demo Walkthrough — 5 Skills Together on a Real Mini Corpus

This walkthrough shows what happens when you actually use the
catalog's skills on a real research task. Every artifact below is in
this repo at
[`test-corpus/ai-agents-social-interaction/`](../test-corpus/ai-agents-social-interaction/) —
nothing is hypothetical, nothing is regenerated for the docs.

The corpus: 5 real papers on AI agents + social interaction, fetched
2026-04-25 via `research-hub search`. Topics cover VR-embodied agents,
LLM theory-of-mind in poker, multi-agent learning, multi-agent
experimentation tooling, and livestreaming alignment.

繁中 README: [../README.zh-TW.md](../README.zh-TW.md). 中文 walkthrough
not yet translated; the artifact files themselves are mostly English.

## Setup (one-time)

```bash
claude plugin marketplace add WenyuChiou/ai-research-skills
bash scripts/install-all.sh        # or pwsh scripts/install-all.ps1
```

After this you have all 5 plugins (13 skills) loaded. Three of them
in this walkthrough need additional setup:

- `research-hub` (paper search) needs `pip install
  research-hub-pipeline` + `research-hub setup`. See
  [install.md](install.md).
- `notebooklm-brief-verifier` Manual fallback works without setup;
  Managed mode needs the research-hub CLI.
- The other 2 here (`literature-triage-matrix`,
  `paper-memory-builder`) are pure-reasoning — install them and
  they're ready.

## Step 1 — Discover papers (`research-hub`)

```text
User: Search for papers on AI agents and social interaction. Find
about 5 with method and domain spread.
```

Claude reaches for the `research-hub` skill, which calls
`research-hub search "AI agents social interaction" --limit 8
--rank-by smart`. The 5 selected papers and their full search-result
JSON live at:

- **[`test-corpus/.../search-results.json`](../test-corpus/ai-agents-social-interaction/search-results.json)**
  — raw search response from Semantic Scholar / arXiv / OpenAlex.
- **[`test-corpus/.../papers/`](../test-corpus/ai-agents-social-interaction/papers/)**
  — one Markdown note per paper with metadata + abstract.

What this demonstrates: the skill picks 5 papers spanning 3 methods
(empirical experiments, frameworks, conceptual) and 5 domains (VR /
health, poker / ToM, education, HCI infrastructure, livestreaming
alignment) — the spread is the falsifiable claim the test corpus
README declares.

## Step 2 — Triage and compare (`literature-triage-matrix`)

```text
User: Compare these 5 papers by method, data, claims, and limitations.
```

Claude triggers `literature-triage-matrix` and reads the 5 paper
notes. Output:

- **[`test-corpus/.../.research/literature_matrix.md`](../test-corpus/ai-agents-social-interaction/.research/literature_matrix.md)**
  — comparison table across `Method`, `Data`, `Central claim`,
  `Limitation`, `Relevance to RQ`.

What this demonstrates: instead of 5 generic per-paper summaries, you
get one table that surfaces the gap (e.g. "all 5 study agents but
only #4 instruments multi-agent experimentation; #5 is a framework
without empirical test"). The matrix is the input to the next step.

## Step 3 — Verify a NotebookLM brief (`notebooklm-brief-verifier`)

```text
User: I uploaded these 5 papers to NotebookLM and got a brief. Verify
it against the source bundle.
```

The skill works in two modes:
- **Managed**: `research-hub` uploaded the bundle + tracked it.
- **Manual fallback**: you paste the downloaded brief + a plain
  source list. Used when the user installs only the marketplace
  plugin (no `research-hub` CLI).

Manual fallback artifacts live in the parallel test corpus:

- **[`test-corpus/manual-fallback-fresh-user/`](../test-corpus/manual-fallback-fresh-user/)**
  — `brief.txt` (the raw NotebookLM output), `sources.md` (the source
  list), and `brief-verify-manual-fallback.md` (the verifier's output:
  missed sources, unsupported claims, contradictions, recommended
  follow-up prompts).

What this demonstrates: a typical NotebookLM brief misses 1-2 sources
silently and contains 1-3 unsupported claims. The verifier flags them
explicitly. Same skill, two input modes, identical output structure.

## Step 4 — Sharpen the research question (`research-design-helper`)

```text
User: Walk me through the research design. RQ: how does theory-of-mind
behavior in LLM agents change with social context?
```

Claude triggers `research-design-helper`, which is a 5-segment
Socratic dialog (RQ → expected mechanism → identifiability check →
validation plan → risk register). Output:

- **[`test-corpus/.../.research/design_brief.md`](../test-corpus/ai-agents-social-interaction/.research/design_brief.md)**
  — one Markdown file with the 5 segments filled in for this RQ.

What this demonstrates: you get a falsifiable design before writing
code. The brief becomes the input to project-context-compressor
(next step) and the model-design step.

## Step 5 — Compress project context (`research-context-compressor`)

```text
User: Compress this project's context so future AI sessions don't
re-read everything.
```

Claude triggers `research-context-compressor` and writes:

- **[`test-corpus/.../.research/project_manifest.yml`](../test-corpus/ai-agents-social-interaction/.research/project_manifest.yml)**
  — research question, datasets, current stage, key entrypoints.
- (Optionally `.research/experiment_matrix.yml` and
  `.research/data_dictionary.yml` for active experimental work.)

What this demonstrates: a future Claude session loads the manifest
in seconds instead of crawling 20+ files. Same effect for human
collaborators picking up the project.

## Step 6 — Build paper memory (`paper-memory-builder`)

```text
User: I have a manuscript draft. Build paper memory before I revise.
```

Claude triggers `paper-memory-builder` over the manuscript file.
Output:

- **[`test-corpus/.../.paper/lim-2025/claims.yml`](../test-corpus/ai-agents-social-interaction/.paper/lim-2025/claims.yml)**
  — every paper-level claim with evidence pointers + status.
- **[`test-corpus/.../.paper/lim-2025/figures.yml`](../test-corpus/ai-agents-social-interaction/.paper/lim-2025/figures.yml)**
  — every figure with key numbers + which claim it supports.
- (After actual revision rounds: `revision_history.yml` —
  append-only audit trail. See the
  [revision_history schema reference](https://github.com/WenyuChiou/research-hub/blob/master/skills/paper-memory-builder/references/revision_history_schema.md).)

What this demonstrates: the writing skill no longer needs to re-read
the manuscript on every audit. `claims.yml` is the shared memory
layer.

## Step 7 — Audit + revise the manuscript (`academic-writing-skills`)

```text
User: Audit this paragraph for banned words, claim-evidence support,
and figure consistency.
```

Claude triggers `academic-writing-skills` with the paragraph + the
`.paper/claims.yml` and `.paper/figures.yml` from Step 6. The skill:

1. Loads `references/banned_words.md` (forbidden GPT-style /
   overclaim phrases).
2. Loads `references/claim_evidence_audit.md`.
3. Cross-checks every numeric claim against `claims.yml` and
   `figures.yml`.
4. Reports: lines with banned phrases, claims without evidence,
   figure references that don't match `figures.yml`.

The skill's reference files (the actual audit logic) live at
[`academic-writing-skills/skills/academic-writing-skills/references/`](https://github.com/WenyuChiou/academic-writing-skills/tree/main/skills/academic-writing-skills/references).
Verification of this skill against real manuscript work is in
[verification.md](verification.md).

What this demonstrates: the chain
`paper-memory-builder → academic-writing-skills` makes audits
incremental. Run paper-memory-builder once per significant revision;
audit per paragraph or per session.

## What this all illustrates

- **Each skill's output becomes the next skill's input.** The chain
  is real (it's why the same `.paper/claims.yml` shows up in both
  paper-memory-builder's output spec and academic-writing-skills'
  input spec).
- **Skills compose without the user wiring them up.** Claude Code's
  auto-trigger picks the right skill from your phrasing; you don't
  have to manually choose.
- **Artifacts persist between AI sessions.** `.research/` and
  `.paper/` directories are the durable memory layer. A new Claude
  session that reads `project_manifest.yml + claims.yml` is up to
  speed in seconds.

## What's NOT in this walkthrough

- `zotero-skills` / `zotero-library-curator` — needs a real Zotero
  library; not on the test corpus.
- `research-hub-multi-ai` — about routing tasks across Claude / Codex
  / Gemini; doesn't produce a single artifact in the corpus.
- `codex-delegate` / `gemini-delegate` — used for downstream code or
  long-context drafting, not in the literature-triage path.
- Real reviewer-response loop with `revision_history.yml` — the
  schema is defined in research-hub's
  `paper-memory-builder/references/revision_history_schema.md`;
  exercising it end-to-end on a real revision round will go in a
  follow-up walkthrough.
