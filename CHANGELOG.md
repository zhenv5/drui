# Changelog

## v1.3.0 — GitHub source-only installation and updates

- Replaced release ZIP installer with `git clone` of the official stable GitHub Tag directly into `~/GameAgentKit`.
- Replaced ZIP SHA-256 updater with GitHub stable-release Tag discovery, official-origin validation, clean-worktree refusal and direct Git checkout. No automatic external Skill updates.
- README / QUICKSTART / clipboard Agent prompts now use GitHub source; CI and Releases no longer publish installer archives.
- No backwards compatibility for legacy ZIP-managed installations (new installation baseline).

# Changelog

## v1.2.1 — Safety and installation audit

- Ensure the bundled `drui` command is executable after ZIP extraction and upgrades; publish it with executable Git mode.
- Validate every HTTPS redirect from GitHub downloads against exact trusted GitHub/CDN hosts; refuse unsafe destinations.
- Upgrade preflight checks all paths before replacement; existing managed files are backed up first and a normal write exception triggers best-effort rollback. Crashes or power loss can still leave partial changes.
- Include CHANGELOG, SECURITY, CONTRIBUTING, and LICENSE in upgrades; fix stale current-version install examples.
- Reject nested directory symlinks in external Skills instead of silently skipping their contents.
- Clarify that Cursor requires explicit selection; `--agents all` retains its previous meaning.
- Add focused regression tests for the above cases.

## v1.2.0 — Copy-to-Agent installation and update prompts

- Added two copy-ready prompts at the top of GitHub README, usable before DRUI is installed; Source of Truth: `prompts/agent-setup/`.
- Added `drui agent install|update`, `drui agent update --copy`, and `drui copy install|update` with platform clipboard detection and explicit failure fallback.
- Prompts require official stable GitHub Release, ZIP SHA-256 verification, dry-run, collision preservation, real acceptance checks, and no silent third-party Skill changes.
- Added regression tests for prompt parity, clipboard success/failure, and read-only generation.


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
