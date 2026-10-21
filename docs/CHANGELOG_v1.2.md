> ARCHIVED history: earlier releases used ZIP. Current releases are GitHub source-only.

# V1.3 — explicit workflow stages and installation documentation

- Clarified `drui` (original GameAgentKit skill) vs user-owned external `oil-ui`.
- Expanded README and QUICKSTART with explicit ZIP extraction, clean installation, safe V1.0/V1.1 upgrade, linking, doctor and original Oil UI registration.
- Added `docs/OIL_UI_USAGE.md` with 15 independent stages, read-only vs implementation behavior, examples and limitations.
- Added `gamekit.py workflow list` / `gamekit.py workflow prompt --stage ... [--project PATH] [--output FILE]` with non-destructive prompt generation and output overwrite protection.
- Added matching instructions under `prompts/drui/stages/` and to `drui/SKILL.md`.
- Existing install/update, link, protection and Oil UI opt-in extension behavior unchanged.
