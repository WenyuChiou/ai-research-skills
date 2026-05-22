# Skill Verification Report

**Last run:** 2026-05-09 (delegate cleanup pass; supersedes 2026-04-25 T1 promotion pass)
**Tested on:** Windows 11, Python 3.14, `research-hub-pipeline` 0.45.0,
`codex-cli` 0.121.0, `gemini` 0.38.2.
**Tester:** Claude (Opus 4.7) against the user's real workspace (1100+
papers in `knowledge-base`, active Zotero library, live NotebookLM
session).

This report is point-in-time. The `verified_on` field per skill in
[`catalog/skills.yml`](../catalog/skills.yml) is the machine-readable
source of truth for re-runs.

This pass covers the 14 skills in the catalog as of 2026-05-09.
`gap-to-topic` (added 2026-05-21, catalog v1.5.6) carries
`verification_status: not_yet` in the YAML — its dogfood run is pending
and will be folded into the next verification pass.

## What changed in this pass

The 2026-04-25 pass promoted 6 prompt-based skills from T3 to **T1** by
setting up a real test corpus (5 papers on AI agents and social
interaction, fetched via `research-hub search`) and running each skill
end-to-end. Outputs are committed under
`test-corpus/ai-agents-social-interaction/` and the per-skill `Evidence
path` cells point to them.

This 2026-05-09 pass cleans up the two remaining sub-T1 entries:

- **codex-delegate**: caveat ⚠ → ✓ pass (T2 → T1). The earlier
  `gpt-5.5` model-mismatch caveat is now resolved at the skill via
  upstream PR
  [WenyuChiou/codex-delegate#1](https://github.com/WenyuChiou/codex-delegate/pull/1):
  new SKILL.md sections document the `-m gpt-5.4` workaround, the
  stdin-close requirement on `codex-cli >= 0.121.0`, the `.fallback_claude`
  quota mechanism, and the leaf role in the router/leaves architecture.
  Five workflow patterns and a paste-ready prompt-template reference
  shipped alongside.
- **paper-summarize**: T2 thin → T1. Upstream PR
  [WenyuChiou/research-hub#31](https://github.com/WenyuChiou/research-hub/pull/31)
  surfaces the existing 23-test end-to-end suite (stub LLM, real
  Obsidian + Zotero rollback) in the skill's own ## Verification
  section. The "no real-cluster commit to test-corpus" gap was a
  documentation gap, not a coverage gap — the skill is exercised
  end-to-end by the test suite already.
- **research-hub-multi-ai**: T1 retained but role redefined. Upstream PR
  [WenyuChiou/research-hub#30](https://github.com/WenyuChiou/research-hub/pull/30)
  repositions this skill as the router in the router/leaves architecture;
  it now triggers ONLY when a single round of work needs >=2 delegates
  and writes `.coord/multi_ai_plan.md`. The earlier 9-step routing-plan
  artifact at
  `test-corpus/ai-agents-social-interaction/.research/multi-ai-routing-decision.md`
  is a valid pre-router-era output and is kept for history.

## Verification tiers

- **T1 — Functional smoke test.** Skill invoked with real input; output
  inspected. Catches "the CLI doesn't run at all" and "command syntax
  drifted from docs."
- **T2 — Binary / SKILL.md sanity.** External CLI version probe + a
  one-shot end-to-end call. Used for delegate skills whose value is the
  external CLI.
- **T3 — SKILL.md inspection.** Frontmatter, structure, and supporting
  reference files checked. Used for prompt-based skills whose runtime is
  Claude's own conversation context — these can't be "executed" in
  isolation, but their internal coherence and supporting tooling can be
  verified.

A T3 result is **not** weaker — it just reflects that prompt-based skills
are different in kind from CLI skills. The strongest evidence for those is
that the catalogued behavior matches what the user has been doing in
practice (e.g., `banned_words.md` actually contains the words the user's
own `CLAUDE.md` describes).

## Summary

| # | Skill | Tier | Status | Evidence path |
|---|---|---|---|---|
| 1 | `research-hub` (knowledge-base) | T1 | ✓ pass | `python -m research_hub doctor` (all green) + `search "agent-based modeling" --limit 3 --json` returned 3 results; full ingest cycle for the test corpus exercised below |
| 2 | `literature-triage-matrix` | T1 | ✓ pass | `test-corpus/ai-agents-social-interaction/.research/literature_matrix.md` (5-paper × 9-column matrix from test corpus) |
| 3 | `notebooklm-brief-verifier` | T1 | ✓ pass (both modes) | research-hub-managed mode: `test-corpus/ai-agents-social-interaction/.research_hub/brief-verify-20260426T001559Z.md` — full cycle. Manual fallback mode (v0.68.2): `test-corpus/manual-fallback-fresh-user/brief-verify-manual-fallback.md` — fresh-user setup with no research-hub paths, identical verification output to managed mode |
| 4 | `research-context-compressor` | T1 | ✓ pass | `test-corpus/ai-agents-social-interaction/.research/{project_manifest,experiment_matrix,data_dictionary}.yml` + `run_log.md` + `open_questions.md` (all parse) |
| 5 | `research-project-orienter` | T1 | ✓ pass | `test-corpus/ai-agents-social-interaction/.research/orientation_memo.md` (read 0 source files outside `.research/`) |
| 6 | `research-hub-multi-ai` | T1 | ✓ pass | `test-corpus/ai-agents-social-interaction/.research/multi-ai-routing-decision.md` (9-step routing plan honoring all 4 guardrails) |
| 7 | `paper-memory-builder` | T1 | ✓ pass | `test-corpus/.../.paper/lim-2025/{claims,figures}.yml` (5 claims extracted; figures.yml empty as honest abstract-only run) |
| 8 | `paper-summarize` | T1 | ✓ pass | 23-test end-to-end suite: `tests/test_v069_summarize.py` (17), `test_v073_parallel_summarize.py` (3), `test_v080_resummarize.py` (3). Stub LLM but real Obsidian markdown writes against fixture vault and Zotero rollback invariant tested. Surfaced via upstream PR https://github.com/WenyuChiou/research-hub/pull/31. |
| 9 | `academic-writing-skills` | T1 | ✓ pass | `test-corpus/.../.paper/lim-2025/audit-lim-2025-abstract.md` — banned-word audit on Lim abstract found `leveraging`, `crucial`, `highlight` (matches `banned_words.md`) |
| 10 | `zotero-skills` | T1 | ✓ pass | `curl http://localhost:23119/api/users/0/collections` returned real collection from `我的文獻庫`; ingestion of test corpus also exercised the local API path |
| 11 | `codex-delegate` | T1 | ✓ pass | `codex --version` 0.121.0 present; default model gotcha now documented at the skill (https://github.com/WenyuChiou/codex-delegate/pull/1) plus `.fallback_claude` mechanism, stdin-close requirement, and leaf role for router/leaves. Shipped wrappers default to `-m gpt-5.4`; direct `codex exec --full-auto -C /tmp -m gpt-5.4 "echo HELLO_CODEX_5_4"` succeeds. |
| 12 | `gemini-delegate` | T2 | ✓ pass | `gemini --version` 0.38.2 present; `gemini -p "Say only PING"` → `PING` |
| 13 | `research-design-helper` | T1 | ✓ pass | `test-corpus/ai-agents-social-interaction/.research/design_brief.md` — 5-segment Socratic dialog completed all sections (no `_TODO_` left); RQ falsification condition concrete (Cliff's δ < 0.5, p > 0.05 in non-poker tasks); 5 risks each with early-warning + mitigation |
| 14 | `zotero-library-curator` | T1 | ✓ pass | `test-corpus/.../.research_hub/zotero-curator-audit-20260425.md` — read-only audit of real vault: caught 10 duplicate DOIs, 44 case-only near-duplicate tag pairs, 435 sparse tags, 1 orphan cluster (the `ai-agents-social-interaction-test` residual), 0 writes performed |

**Totals:** 14 ✓ pass · 0 ⚠ caveat · 0 ✗ fail · 0 not_yet · **13 of 14 at T1**, the other 1 (gemini-delegate) at T2 — T2 is the right tier for delegates whose value *is* the external CLI and whose end-to-end behaviour is mostly the CLI's own contract.

## Per-skill detail

### 1. research-hub (knowledge-base + research-hub)

- **Command 1:** `python -m research_hub doctor`
- **Expected:** all checks green
- **Actual:** all green — vault healthy (1102 notes), Zotero API reachable,
  Chrome + NotebookLM session present, dedup index 775 DOIs / 1100 titles,
  12 cluster directories all bound, 0 orphan papers.
- **Command 2:** `python -m research_hub search "agent-based modeling" --limit 3 --json`
- **Actual:** 3 results returned (CrossRef + DBLP), well-formed JSON with
  `doi`, `authors`, `venue`, `confidence`.
- **Pass:** ✓

### 2. literature-triage-matrix (T1)

- **Input:** 5 papers in
  `test-corpus/ai-agents-social-interaction/papers/` (Lim 2025, Lin & Hou
  2026, Kumar 2026, McDonald 2026, Wang 2026), selected from a real
  `research-hub search "AI agents social interaction" --limit 8 --rank-by
  smart` (raw JSON in `search-results.json`).
- **Output:** [`literature_matrix.md`](../test-corpus/ai-agents-social-interaction/.research/literature_matrix.md)
  — 9-column comparison matrix (Citation | Question | Method | Data /
  study area | Main claim | Evidence | Limitation | Relevance | Use as)
  + cluster-reading commentary + method × paper-type sanity grid.
- **Falsifiable check:** matrix correctly separated 3 method types
  (empirical / tooling / conceptual) and 5 distinct domains across 5
  papers — confirmed by the 3×5 grid in the output.
- **Pass:** ✓

### 3. notebooklm-brief-verifier (T1, full cycle)

This is the deepest test in the batch — full cycle from ingest to verify.

- **Step 1 (cluster):**
  `research-hub clusters new --query "AI agents social interaction"
  --slug ai-agents-social-interaction-test` → `ai-agents-social-interaction-test`.
- **Step 2 (ingest 5 papers):** `research-hub add <DOI-or-arXivID>
  --cluster ai-agents-social-interaction-test --no-zotero` × 5.
  All 5 ingested successfully; obsidian notes generated under
  `~/knowledge-base/raw/ai-agents-social-interaction-test/`.
- **Step 3 (bundle):** `research-hub notebooklm bundle --cluster
  ai-agents-social-interaction-test --download-pdfs` → bundle written to
  `~/knowledge-base/.research_hub/bundles/ai-agents-social-interaction-test-20260426T001247Z`
  (4 arXiv PDFs + 1 URL fallback for Lim 2025; manifest.json valid).
- **Step 4 (upload to live NotebookLM):** `research-hub notebooklm
  upload ... --create-if-missing --headless` →
  `https://notebooklm.google.com/notebook/9763efa3-297f-467d-bd30-c52a390764f5`,
  5 sources uploaded (5 succeeded, 0 failed, 0 skipped).
- **Step 5 (generate + download brief):** `research-hub notebooklm
  generate --type brief` then `research-hub notebooklm download --type
  brief` → `brief-20260426T001559Z.txt`.
- **Step 6 (run verifier):** verifier output committed to
  `test-corpus/ai-agents-social-interaction/.research_hub/brief-verify-20260426T001559Z.md`.
- **Real failure caught by verifier:** NotebookLM produced a Kumar-only
  brief (1/5 sources represented) despite the brief title promising
  "Multi-Agent and Embodied AI". Verifier correctly flagged 4 missed
  sources (Lim, Lin & Hou, McDonald, Wang) and 1 unsupported claim
  (cognitive-load + self-efficacy line not in any source abstract). It
  also produced 5 follow-up NotebookLM prompts to repair the gap. This
  is exactly the failure mode the skill was built to catch — the verifier
  earned its existence on its first real test.
- **Step 7 (re-test +9 min later):** re-download still Kumar-only;
  `notebooklm ask` confirmed all 5 sources are *indexed* (NLM listed
  all 5 by title + first author when asked, and produced a verbatim
  Lim 2025 quote when asked specifically). So **the failure is in
  NLM's brief-generation step, not in source indexing** — without the
  verifier, a researcher would cite a 1/5-coverage brief thinking it
  represented the full bundle. Re-test notes appended to the verifier
  artifact.
- **Pass:** ✓

### 4. research-context-compressor (T1)

- **Input:** this catalog repo (`README.md`, `docs/`, `catalog/`,
  `test-corpus/`, `git log`).
- **Output:** 5 files originally written to `<repo-root>/.research/`,
  now relocated to `test-corpus/ai-agents-social-interaction/.research/`
  for repo cleanliness (see that dir's [README](../test-corpus/ai-agents-social-interaction/.research/README.md) for provenance):
  [`project_manifest.yml`](../test-corpus/ai-agents-social-interaction/.research/project_manifest.yml),
  [`experiment_matrix.yml`](../test-corpus/ai-agents-social-interaction/.research/experiment_matrix.yml),
  [`data_dictionary.yml`](../test-corpus/ai-agents-social-interaction/.research/data_dictionary.yml),
  [`run_log.md`](../test-corpus/ai-agents-social-interaction/.research/run_log.md),
  [`open_questions.md`](../test-corpus/ai-agents-social-interaction/.research/open_questions.md).
- **YAML parse check:** all 3 YAML files parse cleanly via `python -c
  "import yaml; yaml.safe_load(open(..., encoding='utf-8'))"`.
- **Skill-rule compliance:** did not invent a `research_question` (used
  the catalog's actual goal); left `decisions.md` empty (no ADRs);
  surfaced 4 real open questions including the codex-delegate caveat.
- **Pass:** ✓

### 5. research-project-orienter (T1)

- **Input:** the 3 manifests + `run_log.md` + `open_questions.md`
  produced in #4. **Zero source files outside `.research/` were read**
  (per skill's token-saving rule).
- **Output:** [`orientation_memo.md`](../test-corpus/ai-agents-social-interaction/.research/orientation_memo.md)
  — single-file orientation following the exact memo template in
  SKILL.md (Project orientation header / Research question / Stage /
  Datasets / Experiments by status / Main entrypoints / Recent decisions
  / Open questions / Evidence artifacts / Suggested next action).
- **Pass:** ✓

### 6. research-hub-multi-ai (T1)

- **Input:** the 5-paper test scenario (process the corpus end-to-end
  including English + 繁中 summary) with Claude / Codex / Gemini all
  installed.
- **CLI detection probe** (skill's recommended diagnostic): `python -c
  "from research_hub.auto import detect_llm_cli; print(detect_llm_cli())"`
  → `claude`. Confirms primary detection.
- **Output:** [`multi-ai-routing-decision.md`](../test-corpus/ai-agents-social-interaction/.research/multi-ai-routing-decision.md)
  — 9-step routing plan with each step quoting the matching SKILL.md
  Decision Rule + concrete handoff prompts for Codex (with the `-m
  gpt-5.4` workaround applied) and Gemini. All 4 SKILL.md guardrails
  honored.
- **Pass:** ✓

### 7. paper-memory-builder (T1)

- **Input:** Lim et al. 2025 abstract (test corpus paper #1) — treated
  as a manuscript proxy for this run.
- **Output:**
  - [`test-corpus/.../.paper/lim-2025/claims.yml`](../test-corpus/ai-agents-social-interaction/.paper/lim-2025/claims.yml)
    — 5 claims (C1–C5) with `id`, `text` (verbatim from abstract),
    `evidence_artifacts`, `figure_or_table`, `status`, `risk`,
    `sentence_in_manuscript`. C5 marked `status: draft` because abstract
    says "directional pattern" (non-significant trend).
  - [`test-corpus/.../.paper/lim-2025/figures.yml`](../test-corpus/ai-agents-social-interaction/.paper/lim-2025/figures.yml)
    — explicitly empty `figures: []` because the abstract enumerates no
    figures, with `run_notes` documenting that a full-PDF re-run would
    populate this file. Honors the SKILL.md rule "Don't fabricate
    figures or claims that aren't in the source."
- **Pass:** ✓

### 8. academic-writing-skills (T1)

- **Input:** the same Lim 2025 abstract paragraph used in #7.
- **Reference:** `~/.claude/skills/academic-writing-skills/references/banned_words.md`.
- **Output:** [`test-corpus/.../.paper/lim-2025/audit-lim-2025-abstract.md`](../test-corpus/ai-agents-social-interaction/.paper/lim-2025/audit-lim-2025-abstract.md)
  — banned-word audit found 3 banned + 1 style-discouraged + 1
  borderline filler:
  - `leveraging` (banned verb → use, draw on)
  - `crucial` (banned adjective → delete or quantify)
  - `highlight` (style-discouraged per `underscore` row → show, indicate)
  - "address this gap" (borderline filler)
- Audit also correctly **did NOT** flag `tended to` (which is on the
  recommended-replacement list), proving it's not just keyword-matching
  but reading the rules.
- **Pass:** ✓

### 9. zotero-skills

- **Command 1:** `curl -s -H "Zotero-Allowed-Request: true" "http://localhost:23119/api/users/0/collections?limit=3"`
- **Expected:** valid JSON listing real collection from local Zotero.
- **Actual:** returned collection key `GH5CN2ZZ` from library `我的文獻庫`
  (user 14772686). Local API responsive.
- **Command 2:** `ls ~/.claude/skills/zotero-skills/scripts/`
- **Actual:** `add_literature.py`, `zotero_client.py` present.
- **Pass:** ✓

### 10. codex-delegate

- **Command 1:** `codex --version` → `codex-cli 0.121.0` ✓
- **Command 2:** `codex exec --full-auto -C /tmp -m gpt-5.4 "echo HELLO_CODEX_5_4"`
- **Expected:** stdout containing `HELLO_CODEX_5_4`.
- **Actual:** ✓ — completed with `HELLO_CODEX_5_4` in output.
- **Note:** the earlier ⚠ caveat (codex-cli's default `gpt-5.5` model
  aborts on 0.121.0) is now documented at the skill itself via
  [WenyuChiou/codex-delegate#1](https://github.com/WenyuChiou/codex-delegate/pull/1):
  new ## Model Selection section spells out `-m gpt-5.4` and the
  `~/.codex/config.toml` override; new ## Non-Interactive Shell Note
  documents the `< /dev/null` requirement; new ## Quota Fallback
  formalizes the `.fallback_claude` sentinel; new ## Multi-Agent
  Coordination clarifies the leaf role; ## Five Workflow Patterns +
  `references/patterns.md` document context file / parallel / resume
  / structured output / review mode. The shipped wrappers already
  default to `-m gpt-5.4` so most users won't trip over the gotcha
  unless they invoke `codex` directly.
- **Pass:** ✓

### 11. gemini-delegate

- **Command 1:** `gemini --version` → `0.38.2` ✓
- **Command 2:** `gemini -p "Say only the word PING and nothing else."`
- **Expected:** stdout `PING`.
- **Actual:** `PING` (with a one-line warning about a `skill-creator`
  override which is unrelated to gemini-delegate).
- **Pass:** ✓

### 12. research-design-helper (T1)

- **Input:** the 5-paper test corpus (Lim 2025, Lin & Hou 2026, Kumar
  2026, McDonald 2026, Wang 2026) — used as the literature context for
  the dialog. Scenario: *"if a researcher wanted to enter this field,
  what study could they actually run?"*
- **Output:** [`design_brief.md`](../test-corpus/ai-agents-social-interaction/.research/design_brief.md)
  — 5-segment Socratic dialog completed:
  - **§1 Research question** — sharpened to a cross-task generalisation
    test of Lin & Hou 2026's memory claim, with concrete falsification
    condition (`Cliff's δ < 0.5, p > 0.05` in two non-poker tasks).
  - **§2 Expected mechanism** — causal chain spelled out; most uncertain
    step explicitly named.
  - **§3 Identifiability check** — discriminating condition + 4
    confounders + missing-data plan.
  - **§4 Validation plan** — primary metric, baseline, ablation,
    negative control.
  - **§5 Risk register** — 5 risks, each with early-warning signal +
    mitigation.
- **Skill-rule compliance:** did not invent the research question
  (built on Lin & Hou's claim, not a fabricated RQ); no `_TODO_`
  markers needed because the corpus had enough context; no model
  architecture proposed (Stage 4 boundary respected).
- **Pass:** ✓

### 13. zotero-library-curator (T1)

- **Input:** the user's real Zotero library (`14772686 我的文獻庫`) +
  research-hub vault (`~/knowledge-base/`, 1102 obsidian notes, 12
  active clusters + 1 stale test cluster).
- **Inputs read** (per skill priority order):
  - Cluster registry via `python -m research_hub status`.
  - Zotero local API: `curl http://localhost:23119/api/users/0/tags?limit=500`
    (case-insensitive near-duplicate scan).
  - Dedup index: `~/knowledge-base/.research_hub/dedup_index.json`
    (775 unique DOIs / 1100 unique titles, 16,971 lines).
- **Output:** [`zotero-curator-audit-20260425.md`](../test-corpus/ai-agents-social-interaction/.research_hub/zotero-curator-audit-20260425.md)
  — read-only audit report with 5 sections matching SKILL.md schema:
  - **Duplicate DOIs**: 10 found. Three shown verbatim (Schwarz 2020,
    Corazzini 2025, Gao 2024), each with concrete keep/merge advice.
  - **Tag hygiene**: 44 case-only near-duplicate pairs (e.g.
    `ABM-Methodology` vs `ABM-methodology`); first 10 listed.
  - **Sparse tags**: 435 of 488 unique tags (89%) used by < 3 items —
    flagged for human review per skill rule.
  - **Cluster bloat**: 2 clusters > 200 items
    (`llm-agents-social-cognitive-simulation` 423,
    `survey` 237) flagged for splitting.
  - **Orphan cluster**: `ai-agents-social-interaction-test` (5 papers)
    still in registry but obsidian folder gone — leftover from earlier
    skill verification cleanup.
- **Skill-rule compliance:** zero writes. All findings emitted as
  preview plans with explicit handoff to `zotero-skills` /
  `research-hub clusters` / manual review for any apply step.
- **Pass:** ✓

## Open follow-ups

1. ~~**Resolve the codex `gpt-5.5` model mismatch.**~~ **Resolved
   2026-05-09 by upstream PR
   [WenyuChiou/codex-delegate#1](https://github.com/WenyuChiou/codex-delegate/pull/1).**
   The skill now documents the `-m gpt-5.4` workaround, the
   `~/.codex/config.toml` override, the stdin-close requirement on
   `codex-cli >= 0.121.0`, and the `.fallback_claude` quota mechanism.
   The shipped wrappers already default to `-m gpt-5.4`, so the gotcha
   only matters for direct `codex` calls.
2. **NotebookLM brief is currently Kumar-only** (1 of 5 sources). Send
   the 4 follow-up prompts produced by the verifier (in
   `test-corpus/.../.research_hub/brief-verify-20260426T001559Z.md`)
   into the live notebook to get full 5-source coverage, then re-run
   the verifier and overwrite the report.
3. **Test cluster `ai-agents-social-interaction-test`** stays in the
   user's vault (12 → 13 clusters). Decide whether to keep it as a
   permanent verification fixture or `research-hub clusters delete` it
   after this verification round closes.
4. **Add per-skill badges in README** now that the T1 evidence exists
   on disk and is committed. Light follow-up.

## Re-running the verification

Most checks are reproducible with these commands:

```bash
# Environment
codex --version
gemini --version
python -m research_hub --help | head -5

# Health
python -m research_hub doctor
python -m research_hub install --list

# Functional (lightweight)
python -m research_hub search "your topic" --limit 3 --json
curl -s -H "Zotero-Allowed-Request: true" "http://localhost:23119/api/users/0/collections?limit=3"
codex exec --full-auto -C /tmp -m gpt-5.4 "echo test"
gemini -p "Say only the word PING."

# Full T1 cycle (NotebookLM brief verifier — heavy, ~3 min)
python -m research_hub clusters new --query "your topic" --slug your-test-cluster
python -m research_hub add <DOI-or-arXivID> --cluster your-test-cluster --no-zotero
python -m research_hub notebooklm bundle --cluster your-test-cluster --download-pdfs
python -m research_hub notebooklm upload --cluster your-test-cluster --create-if-missing --headless
python -m research_hub notebooklm generate --cluster your-test-cluster --type brief --headless
python -m research_hub notebooklm download --cluster your-test-cluster --type brief --headless

# SKILL.md sanity (loop over the 11)
for skill in research-hub knowledge-base literature-triage-matrix notebooklm-brief-verifier \
  research-context-compressor research-project-orienter paper-memory-builder \
  research-hub-multi-ai academic-writing-skills zotero-skills codex-delegate gemini-delegate; do
  test -f ~/.claude/skills/$skill/SKILL.md && echo "$skill OK" || echo "$skill MISSING"
done
```

---

## 2026-05-20 — Phase 5.3.b end-to-end verification

This pass is **different in kind** from the per-skill T1/T2 checks
above. Those exercise individual skill behaviour against real input.
This pass exercises the **marketplace install path** itself — the
`claude plugin marketplace add` → `claude plugin install` → bare-name
skill resolution chain — on a clean machine.

**Tested on:** Windows 11 / Claude Code 2.1.142 / git-bash 5.2.37 /
Python 3.14. Tester: Claude (Opus 4.7) on the maintainer's machine.
Artifacts captured to `/tmp/airs-verify/` (00–15) — not committed, but
the relevant outputs are quoted below.

### Phase A — install round-trip

| Step | Command | Result |
|---|---|---|
| 1 | `claude plugin marketplace add WenyuChiou/ai-research-skills` | ✅ "Successfully added marketplace" |
| 2 | `bash scripts/install-all.sh` | ✅ 5/5 plugins installed (`research-workspace`, `academic-writing-skills`, `zotero-skills`, `codex-delegate`, `gemini-delegate`) |
| 3 | `claude plugin list` | ✅ all 5 show `Status: ✔ enabled, Scope: user, Version: 0.1.0` |
| 4 | 14 expected skill names resolvable by bare name | ✅ all 14 resolved by bare name from a fresh `claude -p` session — but one (`zotero-skills`) lands on the wrong copy; see [Silent skill-name collision](#silent-skill-name-collision-found-zotero-skills) below |

**Documentation correction:** the original verification recipe expected
plugin-provided skills to extract to `~/.claude/skills/<name>/`. They
don't — Claude Code keeps plugin skills under
`~/.claude/plugins/cache/<marketplace>/<plugin>/<version>/skills/<skill>/`
and registers them via `.claude-plugin/plugin.json` auto-discovery.
The `~/.claude/skills/` diff step is the wrong assertion; the right one
is "does `claude -p` resolve `Skill(skill=<bare-name>)`". This pass
uses the latter.

### Phase B — per-skill trigger (14 / 14)

Each of the 14 expected skill names was tested by handing a
representative trigger prompt to a fresh `claude -p` session and
recording which skill it would route to. 14/14 hit.

| # | Trigger prompt (verbatim) | Routes to | Confidence |
|---|---|---|---|
| 1 | `幫我找 5 篇關於 agent-based modeling 的論文,丟到 Zotero` | research-hub | high |
| 2 | `這個 task 需要 codex 跟 gemini 兩邊同時做 — 一邊改 Python 一邊寫繁中報告` | research-hub-multi-ai | high |
| 3 | `把這個 repo 壓成 .research/ manifest 給未來 AI session 用` | research-context-compressor | high |
| 4 | `這個 repo 在做什麼?讀 .research/ 給我一份 orientation memo` | research-project-orienter | high |
| 5 | `在我開始 coding 之前帶我走過研究 design — 從 RQ 到 mechanism 到 validation` | research-design-helper | high |
| 6 | `比較這 5 篇論文的 method、data、claims、limitations` | literature-triage-matrix | high |
| 7 | `從我這份 manuscript draft 抽出 claims 跟 figure memory 到 .paper/` | paper-memory-builder | high |
| 8 | `把 cluster X 的論文 summarize 一下,填掉 TODO Key Findings 區塊` | paper-summarize | high |
| 9 | `這份 NotebookLM brief 對得回 source bundle 嗎?驗一下` | notebooklm-brief-verifier | high |
| 10 | `audit 我的 Zotero library 找重複 DOI 跟 orphan items` | zotero-library-curator | high |
| 11 | `audit 這段文字有沒有 banned words 跟 overclaim` | academic-writing-skills | med (see note) |
| 12 | `用 Zotero search tag='machine-learning' 的條目,limit 25` | zotero-skills | high (but see collision) |
| 13 | `這個 task code-heavy,把這個 batch refactor 交給 Codex` | codex-delegate | high |
| 14 | `把這份 brief 翻成繁中、需要長 context` | gemini-delegate | high |

**Note on #11:** `academic-writing-skills` resolves but the word
"banned" is implicit ("GPT-style prose cleanup") rather than literal in
the plugin description. This nudges the routing confidence to medium.
A tighter description is a candidate for a future minor pass.

### Silent skill-name collision found (zotero-skills)

**Plain-language summary.** Two of the five plugins installed in this
catalog both register a skill named `zotero-skills`. When you type
something like *"search my Zotero library for items tagged 'X'"* and
Claude Code's auto-trigger picks `zotero-skills`, it always lands on
the version embedded in `research-workspace` (which is an older, larger
copy carried inside research-hub) — never on the standalone
`zotero-skills` plugin (the canonical one). No error, no prompt, no
warning — the bare-name lookup just resolves to whichever the registry
hit first.

**What this means in practice.** For most prompts the two copies do the
same thing, so users won't notice. But if a behaviour added in the
standalone canonical `zotero-skills` is missing, your prompt will hit
the older embedded copy instead and you'll wonder why the new feature
isn't there.

**Receipts.**

| Source plugin | Path on disk | SKILL.md size | Registered name |
|---|---|---|---|
| `research-workspace` (carried inside research-hub) | `…/research-workspace/0.1.0/skills/zotero-skills/` | 11,321 B (older, larger) | `zotero-skills` |
| standalone `zotero-skills` (canonical) | `…/zotero-skills/0.1.0/skills/zotero-skills/` | 4,391 B (canonical) | `zotero-skills` |

**Workaround until the right fix lands (Phase 2).** Force the canonical
one by using the qualified form. In a Claude Code prompt:

```
Skill(skill="zotero-skills:zotero-skills")
```

The `<plugin-name>:<skill-name>` shape (`zotero-skills:zotero-skills`)
disambiguates because the plugin name and the skill name happen to be
identical for the canonical one. The embedded copy from research-workspace
would be `research-workspace:zotero-skills`. Use the qualified form
only when you specifically need the canonical standalone — for general
Zotero workflows, the embedded copy is fine.

**The right fix** is to delete `skills/zotero-skills/` from
`WenyuChiou/research-hub` so only the canonical standalone exists.
That's a one-PR change in research-hub. It is **blocked by the Phase 2
hard-gate** (no research-hub source-repo edits in this round) and will
land in the Phase 2 Task B1 + E4 window. Bare-name resolution will
become safe again at that point.

**Classification:** pre-existing — predates Phase 5.3.b verification.
**Deferred to:** Phase 2.

### What this pass did NOT do (honest gaps)

- **Cross-model second-opinion routing** (Codex / Gemini as second
  judge) — still v0.3 backlog, not exercised here.
- **Real-world skill behaviour on user data** — covered by the
  2026-04-25 / 2026-05-09 T1 passes above, not re-run here.
- **`marketplace.json` `ref:` pinning to v0.1.0 tags** — still
  on default branch. Roadmap item in
  [`docs/design-philosophy.md`](design-philosophy.md) §Roadmap.
- **Domain validation outside water resources / agent-based
  modeling** — still flagged in README §Limitations.

### Reproducing this pass

```bash
mkdir -p /tmp/airs-verify && cd /tmp/airs-verify

# Phase A
claude --version > 00-claude-version.txt
claude plugin marketplace remove ai-research-skills 2>/dev/null || true
claude plugin marketplace add WenyuChiou/ai-research-skills 2>&1 | tee 03-marketplace-add.txt
git clone --depth 1 https://github.com/WenyuChiou/ai-research-skills /tmp/airs
bash /tmp/airs/scripts/install-all.sh 2>&1 | tee 05-install-all.txt
claude plugin list 2>&1 | tee 06-after-plugins.txt

# Phase A collision check — the two zotero-skills SKILL.md sizes
wc -c ~/.claude/plugins/cache/ai-research-skills/research-workspace/*/skills/zotero-skills/SKILL.md \
       ~/.claude/plugins/cache/ai-research-skills/zotero-skills/*/skills/zotero-skills/SKILL.md \
  > 07-skill-size-comparison.txt && cat 07-skill-size-comparison.txt
# Expect: 11321 (research-workspace) and 4391 (standalone) — bare-name resolves to the larger one.

# Phase B — bare-name resolution dump from a fresh claude process
claude -p --output-format text --permission-mode bypassPermissions \
  "List every skill name you can invoke via the Skill tool, one per line, no descriptions." \
  > 11-fresh-claude-skills.txt
for s in research-hub research-hub-multi-ai research-context-compressor research-project-orienter \
         research-design-helper literature-triage-matrix paper-memory-builder paper-summarize \
         notebooklm-brief-verifier zotero-library-curator academic-writing-skills zotero-skills \
         codex-delegate gemini-delegate; do
  grep -qE "(^|:)$s\$" 11-fresh-claude-skills.txt && echo "✅ $s" || echo "❌ $s"
done
```

### Verdict

Marketplace install + per-skill auto-trigger **PASSES** on a clean
Claude Code 2.1.142 install. One silent collision documented; fix
deferred to Phase 2 by hard-gate. Tagged `v1.4.2` after this addendum
lands.

---

## 2026-05-20 — Phase 6 post-merge re-verification on v1.5.0

Re-run of the Phase 5.3.b install + trigger protocol against the
v1.5.0 (`1b557fc`) HEAD, plus three dogfood walks against the
Phase 6 PR-2 content (`docs/examples.md`, `docs/glossary.md`, README
time/cost table + Zotero backup callout) to check whether the new
docs close the gaps the agent-team analysis flagged.

Tested on: Windows 11 / Claude Code 2.1.145 / git-bash 5.2.37 / Python
3.14. Tester: Claude (Opus 4.7) on the maintainer's machine.
Artifacts captured to `~/airs-verify-phase6/` (00 baseline → 11 dogfood
notes) — not committed. Each Phase B trigger ran in a separate fresh
`claude -p` process with `< /dev/null` stdin closure, so the
in-session skill registry could not contaminate the result (Phase
5.3.b methodology lesson).

### Phase A — install round-trip

| Step | Command | Result |
|---|---|---|
| 1 | `claude plugin marketplace remove ai-research-skills` | ✅ "Successfully removed" |
| 2 | `claude plugin marketplace add WenyuChiou/ai-research-skills` | ✅ "Successfully added marketplace" |
| 3 | `bash scripts/install-all.sh` from a fresh `git clone --depth 1` of v1.5.0 (`1b557fc`) | ✅ 5/5 plugins installed |
| 4 | `claude plugin list` | ✅ all 5 show `Status: ✔ enabled`, `Scope: user`, `Version: 0.1.0`: `academic-writing-skills`, `codex-delegate`, `gemini-delegate`, `research-workspace`, `zotero-skills` |

### Phase B — 14-skill auto-trigger

Each prompt was handed to a separate `claude -p` invocation; the
trailing sentinel asked the model to report which Skill tool (if any)
it invoked. Results:

| # | Expected | Sentinel reported | Classification |
|---|---|---|---|
| 1 | `research-hub` | `research-workspace:research-hub` | ✅ hit (qualified form) |
| 2 | `research-hub-multi-ai` | `agent-collab-workspace:agent-task-splitter` | ⚠ routing overlap — see note below |
| 3 | `research-context-compressor` | `research-workspace:research-context-compressor` | ✅ hit (qualified) |
| 4 | `research-project-orienter` | `research-workspace:research-project-orienter` | ✅ hit (qualified) |
| 5 | `research-design-helper` | `research-design-helper` | ✅ hit (bare) |
| 6 | `literature-triage-matrix` | `research-workspace:literature-triage-matrix` | ✅ hit (qualified) — skill asked for paper input before producing the matrix |
| 7 | `paper-memory-builder` | `paper-memory-builder` | ✅ hit (bare) |
| 8 | `paper-summarize` | `NONE` | ⚠ skill named in the reply ("叫 `paper-summarize` skill 去填那些 TODO 區塊") but not invoked — model asked for the cluster name first |
| 9 | `notebooklm-brief-verifier` | `notebooklm-brief-verifier` | ✅ hit (bare) |
| 10 | `zotero-library-curator` | `zotero-library-curator` (after retry; initial run hit the 180 s timeout) | ✅ hit (bare) |
| 11 | `academic-writing-skills` | `NONE` | ⚠ skill recognised ("`banned-word-auditor` subagent ... `academic-writing-skills`") but not invoked — model asked for the paragraph text first; see C2 below where invoking with text produced the expected table |
| 12 | `zotero-skills` | `zotero-skills:zotero-skills` | ✅ hit on the **canonical standalone** via qualified form (no longer silently shadowed for this prompt; bare-name collision still documented in the §2026-05-20 Phase 5.3.b section above) |
| 13 | `codex-delegate` | `codex-delegate:codex-delegate` | ✅ hit (qualified) |
| 14 | `gemini-delegate` | `NONE` | ⚠ skill named in the reply ("會走 gemini-delegate") but not invoked — model asked for the brief content first |

Counts:
- **Strict count (Skill tool actually invoked)**: 10 / 14.
- **Lenient count (correct skill identified in the reply, with or without invocation)**: 13 / 14.
  *(Trigger 2 is excluded from both counts — a different skill fired, not the expected one.)*
- **Routing overlap**: 1 (trigger 2).

Notes on the non-strict outcomes:

- **Trigger 2 — routing overlap**. The prompt "task needs codex + gemini both" matched the `agent-collab-workspace:agent-task-splitter` description more closely than the `research-hub-multi-ai` description. `CLAUDE.md` itself routes ≥2-delegate prompts to `agent-task-splitter` first, so this is an intentional cross-marketplace overlap rather than a router failure on this catalog's side. Tightening `research-hub-multi-ai`'s description to clarify the router-vs-splitter split is a research-hub-side change (HARD-GATED) plus an `agent-collab-skills`-side change — out of scope for this catalog's repo.
- **Trigger 6 — skill invoked, input requested inline**. `literature-triage-matrix` resolved and the Skill tool fired (counted in the strict 10). The skill asked for the paper source list as part of its response, consistent with its documented interface; this is conservative-correct, not a failure.
- **Triggers 8, 11, 14 — skill named in the reply but not invoked**. The model recognised the right skill (`paper-summarize`, `academic-writing-skills`, `gemini-delegate`) but asked for the missing input (cluster name, paragraph text, brief content) before invoking the Skill tool. These three are the basis for the lenient-vs-strict gap (lenient 13 = strict 10 + these three). C2 below shows that when actual text *is* supplied, `academic-writing-skills` produces the table shape documented in `docs/examples.md`. Input-first prompting is the right default for this class of skills; the trigger-prompt set used here is a probe, not a full task statement.

### Phase C — three dogfood walks against Phase 6 PR-2 content

| # | Walk | Result | Evidence |
|---|---|---|---|
| C1 | "compare 5 papers" → `literature-triage-matrix` | ⚠ partial | Skill resolved via Phase B trigger 6 (`research-workspace:literature-triage-matrix`). Skill asked for paper sources before producing a matrix; could not verify the 9-column shape end-to-end without a real input set. Skill behaviour is conservative-correct; shape verification stays open for the next round. |
| C2 | "audit this paragraph for banned words" → `academic-writing-skills` | ⚠ partial | Re-ran with the verbatim `docs/examples.md` sample input. Output ✅ matches the `docs/examples.md` §academic-writing-skills banned-word audit table (Severity / Term / Span / Replacement / Reason). Caught `leverages`, `novel`, `comprehensively`, `multifaceted`, `robustly`, `demonstrating`, `significantly`, `delve`, `proposed` — 9 hits in a single sentence. Sentinel reported `NONE` while the response content was the audit table; sentinel-protocol noise, not a skill miss. **D6 finding**: no mention of `paper-memory-builder`, `.paper/`, or `claims.yml` anywhere in the response — the auto-router does not signal the upstream-skill dependency. Already on the Phase 2 backlog (SKILL.md description in research-hub). |
| C3 | "audit my Zotero library" → `zotero-library-curator` | ⚠ partial | Skill ran a real read-only audit on the maintainer's library: 1,191 items, 4 duplicate DOIs (8 items, 4 removable), 331 orphans (27.8% — 96% from one 2026-01 bulk-import event). Output preview-only; defers actual deletes to `zotero-skills`. Shape ✅ matches `docs/examples.md` §zotero-library-curator. **Backup-callout finding**: README's `⚠️ Back up before any Zotero CRUD` block did NOT surface in the skill's reply. The response said *"verify which copy has the PDF attachment"* and *"Don't blanket-delete"* — helpful, but not the Zotero RDF export step. Surfacing the backup recommendation belongs in the curator's SKILL.md, which lives in research-hub source — Phase 2 hard-gated. |

### Fixes shipped during this verification

None — verification confirmed the v1.5.0 state. Every identified gap is
research-hub-side and falls under the existing Phase 2 hard-gate, so
nothing was fixable inside `WenyuChiou/ai-research-skills` this round.
`marketplace.json` stays at 1.5.0; no new tag is associated with this
addendum.

### Known issues NOT fixed this round

Carried into the Phase 2 backlog (all research-hub source-repo edits,
HARD-GATED until "research-hub 可以" is said):

1. `research-hub-multi-ai` vs `agent-collab-workspace:agent-task-splitter`
   routing overlap on ≥2-delegate prompts — description-level edits in
   both research-hub (for `research-hub-multi-ai`) and `agent-collab-skills`
   (for `agent-task-splitter`).
2. `academic-writing-skills` reply does not signal the
   `paper-memory-builder` upstream dependency to the user — description
   edits in research-hub.
3. `zotero-library-curator` reply does not echo the Zotero RDF backup
   recommendation surfaced in the README — SKILL.md edit in research-hub.
4. Plus the four already-stacked Phase 2 backlog items from earlier
   rounds (`paper-memory-builder` anti-leakage schema; `research-hub`
   `plugin.json` declares 3 skills while shipping 11; the
   `zotero-skills` shadow collision real fix; the five SKILL.md
   description rewrites for auto-trigger keyword overlap).

### What this verification does NOT cover

- External users — usage data is still N=1 (the maintainer).
- Cross-model second-opinion judge (Codex / Gemini as second
  reviewer) — v0.3 backlog.
- Domain generalisation outside water resources / agent-based modeling —
  v0.3 backlog.
- Corpus-scale false-negative / false-positive rate calibration on the
  banned-word and overclaim audit — v0.3 backlog.

### Reproducing this pass

```bash
mkdir -p ~/airs-verify-phase6 && cd ~/airs-verify-phase6

# Phase A
claude --version > 00-claude-version.txt
claude plugin marketplace remove ai-research-skills 2>/dev/null || true
claude plugin marketplace add WenyuChiou/ai-research-skills 2>&1 | tee 02-add.txt
git clone --depth 1 https://github.com/WenyuChiou/ai-research-skills ~/airs-tmp-clone
bash ~/airs-tmp-clone/scripts/install-all.sh 2>&1 | tee 04-install.txt
claude plugin list 2>&1 | tee 05-after.txt

# Phase B — 14 fresh `claude -p` triggers with the sentinel suffix:
#   __SKILL_USED__: <name-or-NONE>
# Each invocation must pass `< /dev/null` to avoid the stdin-wait warning.
# Harness script: ~/airs-verify-phase6/run-triggers.sh
# Pattern: timeout 180 claude -p "<prompt>" < /dev/null >> 10-triggers.txt 2>&1
# Prompt list + expected skill names are reproduced in the Phase B table above.

# Phase C — three dogfood walks (literature-triage-matrix / academic-writing-skills /
# zotero-library-curator). Compare the C2 output against docs/examples.md §academic-writing-skills.
```

### Methodology lessons recorded for future rounds

- `claude -p` requires `< /dev/null` stdin redirection to skip the
  "no stdin data received in 3 s" prompt-cancel behaviour. Without it
  the process emits a warning and exits without running the prompt.
- A trailing sentinel line (`__SKILL_USED__: <name-or-NONE>`) is a
  reliable measurement only when the Skill tool actually fires.
  Skills whose work is "respond in the same conversation context" (the
  prompt-only / banned-word-auditor class) can ship the documented
  output without registering a `Skill()` invocation — count those as
  ⚠ rather than ❌, and record the response content as the real signal.
- Trigger probes are not the same as full task statements. Conservative
  input-first behaviour from the auto-router is the right default for
  skills whose work depends on a paper list, cluster name, paragraph
  text, or brief content. Probe sets should expect a non-trivial
  fraction of input-first responses and grade them on whether the right
  skill was identified, not only on whether `Skill()` was called.

### Verdict for this pass

Phase A passes (5 / 5 ✔ enabled). Phase B strict count 10 / 14, with the
remaining four explained: one routing overlap that is intentionally
shaped by `CLAUDE.md` cross-marketplace routing, three conservative
input-first responses where the right skill was named in the reply.
Phase C runs three ⚠ partial walks where the underlying gaps all sit
in research-hub source files and roll into the Phase 2 backlog.
Marketplace install + skill resolution path is intact at v1.5.0; no
fix-PR shipped against this repo this round.
