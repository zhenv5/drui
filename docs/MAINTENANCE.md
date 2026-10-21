# DRUI GitHub source maintenance

Install from the reviewed official GitHub [source-only Release](https://github.com/zhenv5/drui/releases/latest). No ZIP installer. See [INSTALL_AND_VERIFY.md](INSTALL_AND_VERIFY.md) for the complete manual CLI/Agent workflow, troubleshooting and security boundaries.

```bash
"$HOME/GameAgentKit/scripts/drui" version
"$HOME/GameAgentKit/scripts/drui" verify    # one-line, read-only summary
"$HOME/GameAgentKit/scripts/drui" update --repo zhenv5/drui --check
# Review release changes and make sure git status is clean:
"$HOME/GameAgentKit/scripts/drui" update --repo zhenv5/drui --yes
python3 "$HOME/GameAgentKit/gamekit.py" link --agents codex,claude,antigravity,cursor
"$HOME/GameAgentKit/scripts/drui" verify    # must exit 0
```

Only a successful final `verify` (not merely `install.sh` or `link`) proves that the expected local Skill links have been installed: an existing user-owned same-name Skill is preserved and can cause missing expected links even when the installer exited 0. Four agents use five Skill slots, so the default full check expects 60 links. Use `verify --verbose` for details or `--json` for tooling. The legacy `--agents all` alias does not include Cursor.

`--check` is read-only, and update requires an official origin and clean Git checkout. Checkout is not crash-atomic; inspect status after an interruption, do not forcibly reset user modifications.

DRUI never upgrades third-party Skills. `deps check` requires an opt-in approved fingerprint baseline; the absence of this baseline is not an install failure. Run `deps list` and independently review before optionally using `deps lock`. Successful local verification does not prove real Agent discovery/loading.
