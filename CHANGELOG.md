# Changelog

## v1.1.0 — Beginner-friendly help and workflow discovery (2026-10-20)

- Added `drui start` and useful no-argument `drui help` with goal-based workflow selection, non-execution caveat and Agent chat examples.
- Added `drui list --beginner`, `--category` and `--search` (Chinese/English) while keeping the 20-workflow default menu and backward-compatible `--json` fields.
- `drui help <workflow>` now explains use case, read/write permissions, expected deliverable and an example; typo suggestions and command quick reference.
- New read-only CLI onboarding regression tests. External Skills remain user-owned and are never silently upgraded.
- v1.0.0 is preserved as an immutable historical release; v1.1.0 is independently tagged and packaged.

## v1.0.0 — Initial public release (2026-10-20)

- First public DRUI release, based on the earlier GameAgentKit internal v1.8.0 source snapshot.
- 12 bundled original Skills, 20 independent workflow stages, `drui` CLI and `oil-ui-plus` fallback.
- Install/upgrade scripts for shared multi-Agent skill directories; do not overwrite user-owned Skills.
- Explicit third-party dependency fingerprints (`deps list`, `lock`, `check`, `approve`, `conflicts`), no silent upstream upgrades.
- GitHub Actions test and Release ZIP automation. A SHA-256 checksum provides integrity checking against the published checksum but is not a publisher signature.
- Added `drui version` information command and official `zhenv5/drui` documentation.

Historical internal iteration notes are in `docs/CHANGELOG_v1.*.md` and must not be interpreted as later public releases.
