# DRUI GitHub source maintenance

DRUI is installed from the official GitHub source checkout at `~/GameAgentKit`, pinned to a stable Release tag. No ZIP installation path.

```bash
drui version
drui deps check
drui update --check
# Review upstream commit and changelog first
drui update --yes
python3 ~/GameAgentKit/gamekit.py doctor --agents codex,claude,antigravity,cursor
```

`--check` is read-only. Git checkout must be clean for update; user-modified files or unexpected origin abort. Changes to external Skills are never silently installed/approved. `drui deps lock` creates a local fingerprint baseline after user review; .state/ is gitignored. Updates rely on Git checkout; an interrupted checkout needs human inspection rather than an assumed automatic rollback.
