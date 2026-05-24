# Runtime Contract

This catalog is the skill layer. The executable research workflow lives in
the source repos, especially `research-hub`.

## What Each Layer Does

| Layer | Provides | Does not provide |
|---|---|---|
| `ai-research-skills` catalog | Marketplace registry, install docs, links to canonical `SKILL.md` files | Python CLI, Zotero API access, NotebookLM browser session, MCP server |
| `SKILL.md` files | Portable workflow instructions and output contracts for AI hosts | Guaranteed host auto-triggering or external tool access |
| `research-hub-pipeline` | `research-hub` CLI, MCP/REST server, Zotero/Obsidian/NotebookLM automation, dashboard | Claude Code marketplace install for the whole catalog |

Installing this catalog or copying a `SKILL.md` file does not prove that the
Python runtime is installed. `claude plugin list` only verifies Claude Code
marketplace state.

## Skill Types

| Type | Examples | Runtime expectation |
|---|---|---|
| Prompt-only workflow skills | `gap-to-topic`, `research-design-helper`, `literature-triage-matrix`, `academic-writing-skills` | Any host that can read the needed files and follow the output contract |
| Workspace-file skills | `research-context-compressor`, `research-project-orienter`, `paper-memory-builder` | File-system access to the project or manually supplied context |
| Runtime-backed research automation | `research-hub`, `paper-summarize`, parts of `notebooklm-brief-verifier`, Zotero-backed curation flows | `pip install research-hub-pipeline` plus any required Zotero, Obsidian, NotebookLM, LLM CLI, MCP, or REST setup |
| Deep Zotero CRUD | `zotero-skills` | Zotero local/Web API credentials and a host that can call the API |
| Delegation skills | `codex-delegate`, `gemini-delegate`, `research-hub-multi-ai` | Target CLI installed and available on `PATH`, or a manual handoff prompt |

## Agent Preflight For Literature Search

Before Claude Code, Codex, Gemini CLI, Cursor, OpenClaw, Hermes, or a generic
API client tries to run the literature workflow, verify the executable layer:

```bash
research-hub describe --json
research-hub doctor
research-hub auto "agent-based modeling" --max-papers 3 --no-nlm
```

If `research-hub` is not found:

```bash
pip install research-hub-pipeline
research-hub setup --persona researcher   # or: analyst | humanities | internal
```

If the smoke test stops because no relevance judge is configured, either
install/configure a supported LLM CLI (`claude`, `codex`, `gemini`,
`opencode`, `aichat`, `cursor`, or a custom adapter) or run the smoke test
with `--no-fit-check` and record that relevance filtering was skipped.

Add NotebookLM only after Zotero/Obsidian ingestion works:

```bash
research-hub notebooklm login --auto-detect
research-hub notebooklm bundle --cluster <slug>
research-hub notebooklm upload --cluster <slug>
research-hub notebooklm generate --cluster <slug> --type brief
research-hub notebooklm download --cluster <slug>
```

## Host Compatibility

- Claude Code has the packaged marketplace path and `claude plugin list`.
- Codex, Cursor, Gemini, Windsurf, Hermes, OpenClaw, and generic API clients
  can consume the same `SKILL.md` instructions, but each host needs its own
  discovery or prompt smoke test.
- MCP/REST-capable hosts should prefer `research-hub serve` when they need
  real tool execution instead of a prompt-only workflow.
- OpenClaw is a structurally compatible target through MCP/manual
  `SKILL.md` loading, but this catalog does not claim release-grade
  OpenClaw verification yet.
