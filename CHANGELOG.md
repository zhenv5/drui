# Changelog

## v1.0.0 — Initial public release (2026-10-20)

- First public DRUI release, based on the earlier GameAgentKit internal v1.8.0 source snapshot.
- 12 bundled original Skills, 20 independent workflow stages, `drui` CLI and `oil-ui-plus` fallback.
- Install/upgrade scripts for shared multi-Agent skill directories; do not overwrite user-owned Skills.
- Explicit third-party dependency fingerprints (`deps list`, `lock`, `check`, `approve`, `conflicts`), no silent upstream upgrades.
- GitHub Actions test and Release ZIP automation. A SHA-256 checksum provides integrity checking against the published checksum but is not a publisher signature.
- Added `drui version` information command and official `zhenv5/drui` documentation.

Historical internal iteration notes are in `docs/CHANGELOG_v1.*.md` and must not be interpreted as later public releases.
