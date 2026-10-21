> ARCHIVED **internal GameAgentKit** milestone; this label is historical, not the current public DRUI version. Use [Install & Verify](INSTALL_AND_VERIFY.md) for today's GitHub-only installation.

# GameAgentKit V1.5 — DRUI CLI Quick Commands

- Add safe, reusable terminal entrypoint `scripts/drui`: `list`, `list --json`, `help`, `prompt`, and `<stage>` shorthand (prompt-only in a shell).
- `gamekit.py install/link` now links `~/.local/bin/drui` without overwriting a preexisting command or modifying the user's PATH.
- `gamekit.py unlink` removes only the canonical CLI link actually owned by this kit.
- `drui` Skill now explicitly recognizes `drui list`, `drui help <stage>`, `drui <stage>`, and `drui prompt <stage>` in Agent chats; these use different semantics from shell prompts.
- All 20 workflows listed and grouped in `docs/DRUI_COMMANDS_ZH.md`.
- `gamekit.py workflow list --json` exposes the same single menu registry programmatically. Old commands still work.
- No third-party `oil-ui` files are touched; no paid Pro functionality is claimed.
