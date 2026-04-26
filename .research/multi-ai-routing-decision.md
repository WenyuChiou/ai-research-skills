# Multi-AI routing decision — produced by research-hub-multi-ai

Generated 2026-04-25 for the test scenario: **process the 5-paper
ai-agents-social-interaction corpus end-to-end (search → ingest →
literature matrix → NotebookLM brief → English + 繁中 summary)** while
the user has Claude (primary), Codex CLI (0.121.0), and Gemini CLI
(0.38.2) available.

CLI detection per the skill's own recommended probe:

```bash
$ python -c "from research_hub.auto import detect_llm_cli; print(detect_llm_cli())"
claude
```

So Claude is detected as the primary; Codex and Gemini are present as
delegates.

## Routing decision (per the skill's Roles + Decision Rules)

| Step | Work | Route to | Why (skill's rule) |
|---|---|---|---|
| 1 | `research-hub plan "AI agents social interaction"` | **Claude (primary)** | "Start with `research-hub plan`" — planning is primary's job. |
| 2 | `research-hub auto "AI agents social interaction" --no-nlm` first run | **Claude (primary)** orchestrating, no delegation | Decision Rule: "first-run validation before NotebookLM automation is trusted." |
| 3 | Bundle 5 PDFs and upload to NotebookLM | **Claude (primary)** | Browser-automation step inside research-hub; not a token-heavy LLM call, no delegation needed. |
| 4 | Generate NotebookLM brief | **NotebookLM** (not an LLM CLI choice) | This is NotebookLM-side; brief generation happens server-side at Google. |
| 5 | Write `.research/literature_matrix.md` over 5 papers | **Claude (primary)** | 5 papers is small; primary's domain judgment matters more than token cost. |
| 6 | Crystal generation (long, mechanical synthesis) | **Codex** via `--llm-cli codex` | Decision Rule: "long mechanical crystal generation when Codex is available." |
| 7 | English brief verification (`notebooklm-brief-verifier`) | **Claude (primary)** | Verification needs nuanced judgment — wrong place to delegate. |
| 8 | 繁中 (Traditional Chinese) summary of the brief | **Gemini** via `--llm-cli gemini` | Decision Rule: "Use `research-hub auto ... --llm-cli gemini` when the user explicitly wants Chinese/Japanese/Korean output." Also matches the skill's *Guardrail* — Gemini is preferred for "language-heavy or long-context prose." |
| 9 | Long-form bilingual brief (EN + 繁中 side-by-side) | **Gemini** | Same rule. Long-context + CJK = Gemini. |

## Concrete handoff prompts

### To Codex (step 6)

```bash
codex exec --full-auto -m gpt-5.4 -C "<vault-path>" \
  "Read the 5 paper notes in raw/ai-agents-social-interaction-test/ and \
   generate one crystal note per paper at \
   raw/ai-agents-social-interaction-test/crystals/<slug>.md. \
   Use the research-hub crystal template. Do not invent claims not \
   in the source notes."
```

(Note the `-m gpt-5.4` — required because of the documented codex
caveat in `docs/verification.md`. Without it, `gpt-5.5` aborts.)

### To Gemini (steps 8–9)

```bash
gemini -p "Translate the brief at <brief-path>.md into Traditional \
  Chinese (繁中). Keep all numbers and citations exactly as in the \
  English source. Do not paraphrase or polish — translate only."
```

## Guardrails honored

- Did not delegate planning to Codex/Gemini (skill: "Do not delegate
  before the workflow is clear").
- Did not assume Gemini is Chinese-only — used it for long-context
  bilingual work, which is its real strength (skill: "Do not assume
  Gemini is Chinese-only").
- Did not propose overwriting vault notes or deleting any cluster
  without explicit user approval (skill: "Do not overwrite vault notes
  or delete clusters without explicit user approval"). The proposed
  cluster name `ai-agents-social-interaction-test` is new, not an edit
  to existing 12 clusters.

## Verification

The routing above is **internally consistent with SKILL.md's three
roles + five decision rules + four guardrails**. Specifically:
- Roles table → mapped each step to one of {primary, Codex, Gemini}.
- Decision Rules → quoted the matching rule for each Codex/Gemini call.
- Commands section → used the exact `--llm-cli codex` / `--llm-cli
  gemini` flags the skill names.
- Guardrails → mentioned each one with how the plan honors it.

This is what the skill is *for*: producing a routable plan rather than
"just ask Claude to do it all".
