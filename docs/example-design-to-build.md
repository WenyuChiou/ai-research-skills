# Stage 4 cookbook — from `design_brief.md` to scaffolded code

> **What this example shows.** Stage 4 (*"Design and build the model"*)
> is intentionally **not a dedicated skill** in this catalog. Its input
> is the [`design_brief.md`](example-design-brief.md) from Stage 3a; its
> output is **code in your project** — directory layout, prompt files,
> a runnable experiment skeleton, a test harness, an analysis script.
> Because the output is code (not a YAML manifest with a fixed schema),
> a one-size-fits-all skill would over-constrain the work. Instead the
> handoff is operator-glue, and this cookbook documents it.
>
> Two paths are shown — pick by **scaffold size and how mechanical the
> work is**, not by personal preference:
>
> | Path | When | Tooling |
> |---|---|---|
> | **A. Claude-direct** | ≤ 4 files of scaffold OR judgment-heavy (architecture, decisions about prompt shape, picking a library) | Claude's `Write` / `Edit` tools |
> | **B. codex-delegate** | ≥ 5 files of scaffold AND the pattern is stable (test skeletons, repetitive prompt variants, batch-rename, scripted directory creation) | `codex-delegate` skill — Codex executes, Claude reviews the diff |
>
> Both paths start from the same brief and produce structurally similar
> scaffolds. The choice is about who drives the keyboard, not what the
> output looks like.

## Shared starting point

The input is [`example-design-brief.md`](example-design-brief.md) — a
Stage 3a brief for a research question about LLM agents predicting
household flood-adaptation adoption. Re-read it before either path:

- **Segment 1 (Sharpened RQ)** tells you the **statistical test** the
  experiment must implement (paired DeLong on AUC, threshold ≥ 0.05).
- **Segments 2–3 (mechanism + identifiability)** tell you the **data
  schema** the scaffold must accept (household demographics + prior
  water-use observations + flood history → binary adoption decision).
- **Segment 4 (validation plan)** tells you what **baselines** the
  scaffold must implement alongside the LLM agent (discrete-choice
  logit, rule-based ABM, demographics-only logit, profile-shuffled
  LLM as negative control).
- **Segment 5 (risk register)** tells you what **provenance and
  reproducibility hooks** the scaffold needs (pin LLM model version,
  archive prompts + outputs, fix temperature, record N=10 repeats).

These five reads constrain the scaffold before any file is written.
Both paths use them.

---

## Path A — Claude-direct (no codex)

**When to take this path:**

- The scaffold is **small** (≤ 4 files) — e.g. you're prototyping the
  experimental loop before committing to a full repo layout.
- The work is **judgment-heavy** — e.g. picking between two prompt
  templates, deciding whether to factor a function out, choosing a
  library (PyTorch vs scikit-learn vs raw NumPy) where the brief
  doesn't pin it.
- You want the **iteration loop tight** — Claude edits in-conversation,
  you read the diff, you steer the next edit immediately.

**Example exchange.**

> **Operator:** Read `.research/design_brief.md`. Scaffold the
> minimal-viable experiment — one prompt file, one runnable script,
> one test. Use scikit-learn for the logit baseline, OpenAI Python
> SDK for the LLM agent. Pin `gpt-4o-2024-08-06`. Use the
> 1-week-prototype scope from §1.

> **Claude:** Reading the brief now. Three constraints I'll honour:
> AUC + paired DeLong from §1, profile-shuffled negative control
> from §4, model + temperature pin from §5 risk #5. Proposing four
> files:
>
> | File | Why |
> |---|---|
> | `prompts/household_agent.txt` | The LLM agent system prompt. Profile injected as variables; one file so swap is one edit. |
> | `scripts/run_pilot.py` | 100-household pilot loop: load survey → 70/30 stratified split → run both models → write predictions. |
> | `analysis/auc_delong.py` | Paired DeLong test on the held-out fold (matches §1 falsification condition). |
> | `tests/test_pilot_smoke.py` | One smoke test: 10-household subset runs end-to-end without API calls (mock the LLM client). |
>
> Going to write these now. After: you read the diff, I'll wire in
> the profile-shuffle negative control as a second pass.

The next message is Claude's `Write` calls. The operator reads the
diff and pushes back wherever the scaffold drifts from the brief
(e.g. *"the test should also assert AUC is in [0, 1] before the
DeLong call — segment 4 baseline-3 risk"*).

**Acceptance for Path A** (operator runs after each `Write`):

- `python -m py_compile scripts/run_pilot.py analysis/auc_delong.py`
- `python -m pytest tests/test_pilot_smoke.py -q` (mocked, must pass)
- A diff review: every file maps to a brief segment; nothing scaffolded
  that the brief doesn't justify (the "don't pre-emptively factor"
  rule).

**Why this path is fine for small scaffolds.** When the file count
is low and each file embeds a judgment call, the token cost of
delegating + reviewing usually exceeds the cost of Claude just
doing it. The `codex-delegate` README's
[measured-benefits table](https://github.com/WenyuChiou/codex-delegate/blob/master/skills/codex-delegate/SKILL.md)
lists *"Single-file < 50 line fix — ~1× (don't bother)"* as a
known anti-pattern.

---

## Path B — `codex-delegate` (≥ 5-file scaffold, stable pattern)

**When to take this path:**

- The scaffold is **bigger** (≥ 5 files) — e.g. multiple prompt
  variants per LLM-agent persona, a real test suite (smoke +
  integration + property tests), separate analysis script per
  baseline.
- The pattern is **stable** — once you write the first
  `tests/test_<baseline>_predictive.py`, the next three are mostly
  parameterisation of the same skeleton.
- You're early in the project and want a **canonical layout** to
  start from (a `Cookiecutter`-style baseline you'll then evolve
  by hand).

**Step 1 — write the codex brief.** Place it at
`.ai/codex_task_stage4_scaffold.md` in your project repo:

```markdown
# Codex task: Stage 4 scaffold for LLM-ABM flood-adaptation pilot

## Context
Stage 3a design brief at .research/design_brief.md is the authority.
Re-read it. The pilot RQ requires AUC + paired DeLong on a 70/30
stratified split, with profile-shuffled LLM as a negative control.

## Goal
Create the minimal-viable file tree below. Do NOT implement business
logic beyond stubs — that's the operator's next pass. Every file must
include a top-of-file docstring citing the brief segment it traces to.

## Files to create (exact paths)
- prompts/household_agent_v1.txt       # §1 — base LLM agent prompt
- prompts/household_agent_shuffled.txt # §4 negative control variant
- data/household_schema.yml            # §2 — feature schema
- scripts/run_pilot.py                 # main loop (stub)
- scripts/run_negative_control.py      # profile-shuffle variant (stub)
- analysis/auc_delong.py               # §1 falsification test
- analysis/baseline_logit.py           # §4 baseline 1 (logit)
- analysis/baseline_rules.py           # §4 baseline 2 (rule-based ABM)
- tests/test_pilot_smoke.py            # mock-API smoke test
- tests/conftest.py                    # shared LLM mock fixture

## Constraints
- Python 3.11+, scikit-learn for logits, OpenAI Python SDK pinned to
  gpt-4o-2024-08-06 (§5 risk #5).
- No real API calls in tests — use the mock fixture from conftest.py.
- Each script writes outputs under outputs/<run_id>/ (provenance from
  §5 risk #5: archive prompts + outputs).
- Do NOT touch .research/ or .paper/ — those are read-only manifests.

## Acceptance
- `python -m py_compile $(git ls-files '*.py')` succeeds.
- `python -m pytest tests/test_pilot_smoke.py -q` passes (mocked).
- `grep -rl "design_brief" prompts data scripts analysis tests | wc -l`
  returns ≥ 10 (every scaffolded file cites the brief — one integer,
  not per-file counts).
```

**Step 2 — invoke the wrapper.** From Claude Code Bash:

```bash
bash ~/.claude/skills/codex-delegate/scripts/run_codex.sh \
  --prompt "Read .ai/codex_task_stage4_scaffold.md and execute all instructions inside." \
  --repo "$PWD" \
  --log-file .ai/codex_log_stage4_scaffold.txt
```

(Or, equivalently in the operator's session:
`Skill("codex-delegate", args="brief=.ai/codex_task_stage4_scaffold.md")`.)

**Step 3 — read the structured result.**

```bash
cat .ai/codex_log_stage4_scaffold.txt.result.json
```

Look for `status: success` and inspect `files_changed`. If `status`
is `fallback`, Codex hit its quota and Claude needs to take over —
that's why the brief includes exact paths and a tight acceptance
spec.

**Step 4 — Claude reviews the diff.** Mandatory per the Complex
Task Protocol:

```bash
git status --short             # 10 new files expected
git diff --stat                # +N lines per file
python -m py_compile $(git ls-files '*.py')
python -m pytest tests/test_pilot_smoke.py -q
grep -rl "design_brief" prompts data scripts analysis tests | wc -l
```

Reject (`git restore .`) and re-spec if Codex:
- Scaffolded a file the brief didn't ask for (F11 — over-application).
- Skipped a brief citation in a docstring (acceptance criterion violated).
- Called the real API in tests instead of using the mock fixture.
- Touched `.research/` or `.paper/` (constraint violation).

**Step 5 — commit.** Each agent boundary is a commit boundary
(per the global Multi-Agent Collaboration rule), so the scaffold
gets its own commit before you start filling in business logic.

**Acceptance for Path B** (same as Path A, plus delegation-specific):

- The five Step-4 commands all pass.
- The `.result.json` `risks` list is empty or explained.
- A `code-reviewer` pass on the commit verifies the brief→file
  mapping is 1:1 (trigger 1 fires: ≥ 5 files).

---

## Decision table (one more time, condensed)

| Question | If YES → Path A | If YES → Path B |
|---|---|---|
| Is the file count ≤ 4? | ✅ | |
| Does every file embed a judgment call? | ✅ | |
| Am I picking architecture / libraries the brief doesn't pin? | ✅ | |
| Do I need tight iteration on the prompt shape itself? | ✅ | |
| Is the file count ≥ 5? | | ✅ |
| Is the pattern stable (1st file → others by parameterisation)? | | ✅ |
| Am I creating a canonical layout to evolve later? | | ✅ |
| Mix of mechanical + judgment? | | **Split**: codex-delegate for the mechanical files, Path A for the judgment files; both gated by the same `code-reviewer` pass. |

The decision is not "Claude can't do bulk work" or "Codex can't
think" — it's about where the token cost lands. Mechanical bulk
on Claude is wasteful; judgment-heavy work on Codex drifts (see
the `codex-delegate` F11/F12 anti-patterns).

---

## Anti-patterns to watch

| ❌ Don't | ✓ Do |
|---|---|
| Skip re-reading `design_brief.md` because *"I remember what it said"* | Re-read it before writing the codex brief or the first `Write` call. Brief segments encode acceptance constraints (e.g. paired DeLong, profile-shuffle, model pin) that scaffolds silently miss when you go from memory. |
| Send Codex an open-ended *"scaffold a Stage 4 experiment"* prompt | Always include the **exact file paths** + **acceptance commands** in the brief. F11 (Codex over-applies a sweep rule to docs about the rule) is what under-specified briefs cause. |
| Let Codex implement business logic in the first pass | First pass = stubs + docstrings citing brief segments. Business logic is a second commit, often Path A. Keeps the diff reviewable. |
| Commit scaffold without a `code-reviewer` run | ≥ 5 new files triggers the mandatory `code-reviewer` gate (CLAUDE.md trigger #1). Skip = lesson cost from v0.88.15 (4 P1 bugs hidden behind green tests). |
| Mix scaffold work with later business-logic work in one commit | Each agent boundary is a commit boundary. Scaffold = its own commit. Business logic = another commit. `git blame` should attribute correctly. |
| Use the cookbook to justify *not* writing a `design_brief.md` first | If you have no brief, you have nothing to scaffold against. Run Stage 3a `research-design-helper` first. |

---

## Cross-references

- Input: [`example-design-brief.md`](example-design-brief.md) (Stage 3a)
- Upstream wire: [`example-topic-dossier.gaps.yml`](example-topic-dossier.gaps.yml) →
  brief frontmatter `source: topic_dossier.gaps.yml#G2` →
  (Stage 4) every scaffolded file's docstring cites `design_brief §<N>`.
- Downstream wire: After Path A or B produces the scaffold, Stage 5
  uses [`example-project-manifest.yml`](example-project-manifest.yml)
  to compress run context across sessions. The manifest's
  `research_question` is the same sentence that segment-1 of the
  scaffold's docstrings should cite — verbatim, per the
  Stage 3a → 3b verbatim-mirror contract.
- Delegate skill docs: see the
  [`codex-delegate` SKILL.md](https://github.com/WenyuChiou/codex-delegate/blob/master/skills/codex-delegate/SKILL.md)
  for wrapper invocation, the `.result.json` schema, and the
  measured-benefits table that quantifies *"~1× (don't bother)"*
  for small fixes.
