# Skill Verification Report

**Last run:** 2026-04-25
**Tested on:** Windows 11, Python 3.14, `research-hub-pipeline` 0.45.0,
`codex-cli` 0.121.0, `gemini` 0.38.2.
**Tester:** First-pass verification by Claude (Opus 4.7) against the user's
real workspace (1100+ papers in `knowledge-base`, active Zotero library,
NotebookLM Chrome session present).

This report is point-in-time. The `verified_on` field per skill in
[`catalog/skills.yml`](../catalog/skills.yml) is the machine-readable
source of truth for re-runs.

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

| # | Skill | Tier | Status | Notes |
|---|---|---|---|---|
| 1 | `research-hub` (knowledge-base + research-hub) | T1 | ✓ pass | doctor green; search returned 3 real results |
| 2 | `literature-triage-matrix` | T3 | ✓ pass | SKILL.md well-formed; relies on real Zotero/Obsidian inputs already verified |
| 3 | `notebooklm-brief-verifier` | T3 | ✓ pass | SKILL.md well-formed; chrome + nlm_session healthy in doctor |
| 4 | `research-context-compressor` | T3 | ✓ pass | SKILL.md well-formed; foundation for #5 |
| 5 | `research-project-orienter` | T3 | ✓ pass | SKILL.md well-formed; deferred to #4 if `.research/` missing |
| 6 | `research-hub-multi-ai` | T3 | ✓ pass | SKILL.md present; routing rules consistent with installed codex/gemini |
| 7 | `paper-memory-builder` | T3 | ✓ pass | SKILL.md well-formed; downstream of academic-writing-skills |
| 8 | `academic-writing-skills` | T3 | ✓ pass | SKILL.md + 7 reference files including `banned_words.md` (4/4 spot-checked words present) |
| 9 | `zotero-skills` | T1 | ✓ pass | Zotero local API returned a real collection ("我的文獻庫"); scripts present |
| 10 | `codex-delegate` | T2 | ⚠ caveat | `codex-cli 0.121.0` present; default model `gpt-5.5` requires newer CLI — passing `-m gpt-5.4` works |
| 11 | `gemini-delegate` | T2 | ✓ pass | `gemini 0.38.2` present; one-shot prompt returned `PING` cleanly |

**Totals:** 10 ✓ pass · 1 ⚠ caveat · 0 ✗ fail · 0 not_yet.

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

### 2. literature-triage-matrix

- **Command:** SKILL.md inspection (prompt-based; runs inside Claude's context).
- **Checked:** valid YAML frontmatter (name, description), 113 lines, 6
  section headers including When-to-use / Output schema / What NOT to do.
  Underlying inputs (Zotero collections, Obsidian clusters) verified working
  in #1 and #9.
- **Pass:** ✓

### 3. notebooklm-brief-verifier

- **Command:** SKILL.md inspection + supporting tooling check.
- **Checked:** valid frontmatter, 134 lines, 14 section headers. Doctor
  confirms `chrome: Available via patchright` and `nlm_session:
  C:\Users\wenyu\knowledge-base\.research_hub\nlm_sessions\default` exist
  with no orphan Chrome process.
- **Caveat:** I did not download a fresh NotebookLM brief and run the full
  verifier loop end-to-end (would have needed Chrome automation against a
  live brief). T3 only.
- **Pass:** ✓ (with the T3 limitation noted)

### 4. research-context-compressor

- **Command:** SKILL.md inspection.
- **Checked:** valid frontmatter, 108 lines, 7 sections including
  Inputs-to-read / Outputs-to-produce / Schema-reference / Token-saving
  behavior / What-NOT-to-do. Foundation skill — its outputs feed #5.
- **Pass:** ✓

### 5. research-project-orienter

- **Command:** SKILL.md inspection.
- **Checked:** valid frontmatter, 120 lines, 7 sections. Skill explicitly
  defers to #4 if `.research/` doesn't exist (correct dependency direction).
- **Pass:** ✓

### 6. research-hub-multi-ai

- **Command:** SKILL.md inspection + delegate-CLI check.
- **Checked:** valid frontmatter, 47 lines (shortest of the set, but covers
  Roles / Decision Rules / Delegation patterns). Routing rules name `codex`
  and `gemini` — both binaries verified present in #10 and #11.
- **Pass:** ✓

### 7. paper-memory-builder

- **Command:** SKILL.md inspection.
- **Checked:** valid frontmatter, 125 lines, 8 sections. Explicitly *not for*
  writing the manuscript itself — clean boundary with #8.
- **Note:** I did not run it end-to-end against a real manuscript directory;
  doing so would have required picking a Yang-group paper and writing
  `.paper/claims.yml` files into it. Acceptable for first-pass T3.
- **Pass:** ✓

### 8. academic-writing-skills

- **Command 1:** SKILL.md inspection.
- **Checked:** valid frontmatter, 114 lines, 10 sections. Defers
  abstract-only work to `abstract-writer` and critique-only to
  `professor-yang-review` — correctly bounded.
- **Command 2:** `references/` directory inventory.
- **Checked:** 7 reference files present (`banned_words.md`,
  `figure_conventions.md`, `journal_format_template.md`,
  `section_checklists.md`, `style_overrides_example.md`,
  `submission_checklist.md`, `writing_principles.md`).
- **Command 3:** spot-check `banned_words.md` against the words the user's
  own global `CLAUDE.md` cites.
- **Expected:** "preferentially", "delve into", "systematically", "filter
  tightens" all present.
- **Actual:** all 4 found.
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
- **Command 2:** `codex exec --full-auto -C /tmp "echo HELLO_FROM_CODEX"`
- **Expected:** stdout containing `HELLO_FROM_CODEX`.
- **Actual:** ✗ — Codex aborts with
  `The 'gpt-5.5' model requires a newer version of Codex. Please upgrade
  to the latest app or CLI and try again.` The user's default codex model
  is configured as `gpt-5.5` somewhere (likely `~/.codex/config.toml`).
- **Command 3:** `codex exec --full-auto -C /tmp -m gpt-5.4 "echo HELLO_CODEX_5_4"`
- **Actual:** ✓ — completed with `HELLO_CODEX_5_4` in output.
- **Workaround:** explicitly pass `-m gpt-5.4` until codex-cli is upgraded
  to a version that supports `gpt-5.5`. Or update `~/.codex/config.toml`
  to use `gpt-5.4` until the CLI catches up.
- **Pass:** ⚠ caveat — skill itself is fine; the Codex CLI install needs
  either an upgrade or a model-version override.

### 11. gemini-delegate

- **Command 1:** `gemini --version` → `0.38.2` ✓
- **Command 2:** `gemini -p "Say only the word PING and nothing else."`
- **Expected:** stdout `PING`.
- **Actual:** `PING` (with a one-line warning about a `skill-creator`
  override which is unrelated to gemini-delegate).
- **Pass:** ✓

## Open follow-ups (out of scope for this verification pass)

1. **Resolve the codex `gpt-5.5` model mismatch.** Either upgrade
   `codex-cli` past 0.121.0 or pin the default to `gpt-5.4` in
   `~/.codex/config.toml`. Once fixed, re-run #10 and update the YAML
   `verification_status` from `caveat` back to `pass`.
2. **Promote 4 T3 skills to T1** by running real end-to-end invocations:
   - `literature-triage-matrix` against a 5-paper Obsidian cluster.
   - `notebooklm-brief-verifier` against a freshly-downloaded brief.
   - `research-context-compressor` against this very catalog repo
     (would also create the catalog's own `.research/` files).
   - `paper-memory-builder` against one Yang-group paper directory.
3. **Add per-skill badges in README** once T3 → T1 promotions land.

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

# Functional
python -m research_hub search "your topic" --limit 3 --json
curl -s -H "Zotero-Allowed-Request: true" "http://localhost:23119/api/users/0/collections?limit=3"
codex exec --full-auto -C /tmp -m gpt-5.4 "echo test"
gemini -p "Say only the word PING."

# SKILL.md sanity (loop over the 11)
for skill in research-hub knowledge-base literature-triage-matrix notebooklm-brief-verifier \
  research-context-compressor research-project-orienter paper-memory-builder \
  research-hub-multi-ai academic-writing-skills zotero-skills codex-delegate gemini-delegate; do
  test -f ~/.claude/skills/$skill/SKILL.md && echo "$skill OK" || echo "$skill MISSING"
done
```
