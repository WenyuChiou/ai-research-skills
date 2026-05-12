# Hermes Install Summary

**Date**: 2026-05-10
**Host**: WSL2 Ubuntu on Windows 11
**Hermes version**: 0.13.0 (2026.5.7) [6e5c49bd]
**Installer source**: `https://raw.githubusercontent.com/NousResearch/hermes-agent/main/scripts/install.sh` (1647 lines)

## Install command

```bash
export HERMES_HOME="$HOME/hermes-compat-test"
export PATH="$HOME/.local/bin:$PATH"
mkdir -p "$HOME/.local/bin"
setsid bash install.sh --skip-setup </dev/null > install.log 2>&1
```

Three deliberate isolation techniques:

1. **`HERMES_HOME` override** — divert install state to a side directory instead of `~/.hermes/` so the experiment is fully reversible by deleting one folder.
2. **rc-isolation trick** — pre-create `~/.local/bin` and put it first in `PATH` so the installer's L1130–1242 rc-modification logic detects the bin already on PATH and short-circuits. Result: `.bashrc` / `.profile` SHA256 unchanged after install (proof in `rc-integrity.md`).
3. **`setsid` + `</dev/null`** — detach from controlling terminal so the installer's `(: </dev/tty) 2>/dev/null` probe returns false, falling through to the non-interactive code path that **logs a warning and skips** the optional sudo install of ripgrep/ffmpeg instead of hanging on a prompt.

## Outcome

- Exit code: 0
- Install log: 207 lines
- Total time: ~1 minute (wall-clock)
- No prompts, no sudo, no rc modification

## Install layout

`HERMES_HOME` (~/hermes-compat-test/) received:

```
.env  config.yaml  SOUL.md
hermes-agent/   (Python venv + source — 36 subdirs)
node/           (Node 22 bundled tarball)
hooks/  cron/   sessions/  logs/  memories/  pairing/
audio_cache/    image_cache/
skills/         (26 bundled skill categories)
```

**`~/.hermes/` does NOT exist** — HERMES_HOME redirect was fully respected for the base install.

CLI launcher landed at `~/.local/bin/hermes` (a small Python shim that points at the venv).

## Skipped optional packages

Installer detected `ripgrep` and `ffmpeg` missing on PATH. Because stdin was `</dev/null` and `/dev/tty` was unavailable (due to `setsid`), it took the non-interactive branch (install.sh L800):

```
log_warn "Non-interactive mode and no terminal available — cannot install system packages"
log_info "Install manually after setup completes: sudo $install_cmd"
```

This is the **designed graceful fallthrough**. Hermes still installed cleanly; only the optional accelerators were skipped.

## Final installer message

```
✓ Installation Complete!

📁 Your files:
   Config:    /home/wenyu/hermes-compat-test/config.yaml
   API Keys:  /home/wenyu/hermes-compat-test/.env
   Data:      /home/wenyu/hermes-compat-test/cron/, sessions/, logs/
   Code:      /home/wenyu/hermes-compat-test/hermes-agent
```

Confirms `HERMES_HOME` override worked end-to-end.
