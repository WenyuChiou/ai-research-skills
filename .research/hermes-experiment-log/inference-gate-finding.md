# Inference Gate Finding

## What we tried

```bash
hermes -z "make a literature matrix for these 3 papers: arXiv:2604.04157, arXiv:2604.02677, arXiv:2604.18850"
```

The trigger phrase "make a literature matrix" is the exact first bullet of the skill's `## When to use` section. If Hermes' router works as expected, this prompt should dispatch through the `literature-triage-matrix` skill.

## What happened

```
hermes_cli.auth.AuthError: No inference provider configured. Run 'hermes model'
to choose a provider and model, or set an API key (OPENROUTER_API_KEY,
OPENAI_API_KEY, etc.) in ~/.hermes/.env.
```

Hermes raised the auth error **before** any prompt assembly, in the runtime-provider resolution step (`hermes_cli/runtime_provider.py:966` → `hermes_cli/auth.py:1468`).

## Decision: stop here

Entering an inference-provider API key was out of scope for this audit. The Hermes installer pulled no Anthropic / OpenAI / OpenRouter credentials of its own, and supplying user credentials would shift the experiment from "does the skill format work" to "does my account work" — a different question and not the one the user asked.

## What this does and does not validate

**Does validate** (evidence above + in `skill-install-transcript.md`):

- ✅ Hermes' agentskills.io implementation accepts a strict-minimum frontmatter (`name` + `description` only).
- ✅ Hermes' security scanner returns SAFE for our skill body.
- ✅ The skill registers in `hermes skills list`, `hermes dump`, and re-passes `hermes skills audit`.
- ✅ Hermes' URL-based install path is the documented `hermes skills install <github-raw-url>` and works first-try.

**Does not validate**:

- ❌ Whether Hermes' actual LLM-routing dispatches a triggering prompt through this specific skill (couldn't reach the prompt-assembly layer without auth).
- ❌ Whether the resulting matrix has the same shape as the Claude Code reference matrix in `test-corpus/ai-agents-social-interaction/.research/literature_matrix.md` (no run, no comparison possible).
- ❌ Whether the skill's prose ("write to `<project-root>/.research/literature_matrix.md`") is interpreted by Hermes' tool layer the same way Claude Code interprets it. Both are valid "compatible with agentskills.io" implementations and may diverge on side effects.

## Calibrated claim shape

For portfolio / LinkedIn purposes, the supportable claim is:

> Skills authored to the open agentskills.io spec install cleanly into Hermes Agent (`hermes skills install <github-raw-url>`), pass its security scan, and register in its skills subsystem — verified end-to-end on `literature-triage-matrix` from research-hub.

**Not** supportable from this experiment alone:

> Skills produce the same output on Hermes as on Claude Code.

To upgrade to the stronger claim, a follow-up session with auth + a second-corpus rerun would be needed.

## Why this is still a real result

The premise being tested was: "agentskills.io is a real open standard, and our skills are portable to it, not just Claude-Code-specific". The install-layer evidence settles that. Bottom-half of the agent stack (the LLM-routing + tool-call layer) is per-host behavior anyway — the user's interest was in the *spec* portability, not in proving Hermes' router is bug-free.
