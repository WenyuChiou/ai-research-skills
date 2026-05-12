# rc File Integrity Proof

**Question being answered**: did the Hermes installer modify any shell rc file?

## Method

Snapshot SHA256 of every rc file Hermes' installer touches (per its L1130–1242 path-modification block):
- `~/.bashrc`
- `~/.zshrc`
- `~/.bash_profile`
- `~/.profile`
- `~/.config/fish/config.fish`

Compare before and after install.

## Pre-install snapshot (2026-05-10, before installer ran)

```
342099da4dd28c394d3f8782d90d7465cb2eaa611193f8f378d6918261cb9bb8  /home/wenyu/.bashrc
MISSING /home/wenyu/.zshrc
MISSING /home/wenyu/.bash_profile
28b4a453b68dde64f814e94bab14ee651f4f162e15dd9920490aa1d49f05d2a4  /home/wenyu/.profile
MISSING /home/wenyu/.config/fish/config.fish
```

## Post-install snapshot (after `hermes --version` succeeds + skill install succeeds)

```
342099da4dd28c394d3f8782d90d7465cb2eaa611193f8f378d6918261cb9bb8  /home/wenyu/.bashrc
MISSING /home/wenyu/.zshrc
MISSING /home/wenyu/.bash_profile
28b4a453b68dde64f814e94bab14ee651f4f162e15dd9920490aa1d49f05d2a4  /home/wenyu/.profile
MISSING /home/wenyu/.config/fish/config.fish
```

## Diff

Byte-identical. **Zero rc modification.**

## Why this matters

The Hermes README documents the installer "modifies PATH via .bashrc/.zshrc on Linux/macOS/WSL2/Termux". The user's standing rule is: stop before doing that, ask first.

The **rc-isolation trick** — pre-create `~/.local/bin` and put it first in `$PATH` before invoking the installer — exploits the installer's L1180 check:

```bash
# pseudocode of L1180
if echo "$PATH" | grep -q "^$HOME/.local/bin"; then
    log_info "~/.local/bin already on PATH; skipping rc modification"
    return
fi
```

Because the directory was already on PATH from our `export PATH="$HOME/.local/bin:$PATH"`, the installer skipped the rc-write branch entirely. Verified by SHA256 above.

## Cleanup verifies the same property

After the experiment, removing `~/.hermes/`, `~/hermes-compat-test/`, and `~/.local/bin/{hermes,node,npm,npx,uv,uvx,python3.11}` restores the system fully. No rc files to revert because none were touched.
