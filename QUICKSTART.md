# DRUI Quickstart · GitHub source installation

DRUI is a set of 12 bundled Skills and 20 independent workflows for game UI/UX development and QA. Python 3 and Git are required. **No ZIP installer is supported.**

## First install from official GitHub tag

Visit https://github.com/zhenv5/drui/releases/latest and choose the newest stable tag `vX.Y.Z`. Run:

```bash
git clone --depth 1 --branch v1.3.0 https://github.com/zhenv5/drui.git "$HOME/GameAgentKit"
bash "$HOME/GameAgentKit/install.sh" --agents codex,claude,antigravity,cursor --dry-run
bash "$HOME/GameAgentKit/install.sh" --agents codex,claude,antigravity,cursor
python3 "$HOME/GameAgentKit/gamekit.py" doctor --agents codex,claude,antigravity,cursor
"$HOME/GameAgentKit/scripts/drui" start
```

Replace `v1.3.0` with the latest **verified stable release Tag** when a newer version is published. Git checks out the tagged source locally (often detached HEAD). For the terminal command `drui`, add `~/.local/bin` to PATH if necessary. An existing `~/GameAgentKit` is never overwritten by the bootstrap instructions.

## Update directly from GitHub (no archive)

```bash
drui update --repo zhenv5/drui --check
drui update --repo zhenv5/drui --yes
drui version
python3 "$HOME/GameAgentKit/gamekit.py" doctor --agents codex,claude,antigravity,cursor
```

`--check` does not touch local Git state. `--yes` only updates a **clean Git checkout**, fetching the official stable release tag and switching to its validated commit. No `git reset --hard`, `git pull` over local changes, third-party installer execution or third-party Skill upgrade. Source updates aren't crash-atomic; review your `git status` before a retry if interrupted.

## First task

```bash
drui start
drui list --beginner
drui help usability-review
drui prompt review-loop
```

The terminal prints prompts; it does not execute an AI Agent. Paste a prompt into Codex, Claude Code, Antigravity or Cursor. To copy Agent setup instructions from an existing installation: `drui copy install` or `drui copy update`.

## External Skills

```bash
drui deps list
drui deps conflicts
drui deps lock  # only after reviewing installed sources
drui deps check
```

The lock file is local (`~/GameAgentKit/.state/`, excluded from Git). No third-party Skill is installed, overwritten or upgraded by DRUI. Verify the actual Agent loading outcome independently.
