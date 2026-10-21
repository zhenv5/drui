# Changelog

## v1.4.4 — TL and first-time user onboarding audit

- Make `--agents all` mean all four supported Agents, consistent with default verification.
- Make `install.sh` and `gamekit.py link` fail with nonzero status if final Skill verification is incomplete; never overwrite existing user Skills.
- Clarify one-Agent install/verify scopes; simplify README first-use path and add a safe read-only first workflow.
- Add separate TL and novice-lens audit evidence, explicit regression checks and GitHub CI coverage.

## v1.4.3 — Documentation-wide Tech Lead audit

- Correct current GitHub Tag installation examples, four-Agent verification instructions, source release contribution workflow, and third-party baseline guidance.
- Distinguish historical internal GameAgentKit milestones from public DRUI releases and remove the obsolete, manually triggerable ZIP publishing workflow.
- Add a reproducible maintainer release checklist, review report, and automated Markdown-local-link/version/command consistency checks.
- Preserve existing CLI and Skill behavior; actual Agent runtime loading still requires machine-level testing.

## v1.4.2 — Install docs and Tech Lead audit

- Consolidate GitHub CLI/Agent install, update, compact verification, troubleshooting and trust boundaries in `docs/INSTALL_AND_VERIFY.md`.
- Fix shell snippets so installation failures retain nonzero exit codes; require successful `drui verify` after intentionally skipped name collisions.
- Remove stale ZIP/SHA-256 upgrade claims from `SECURITY.md` and old release instructions from the user manual.
- Clarify 4 agents / 5 Skill paths / 60 links, optional deps baseline, PATH warning, and real-Agent-loading limitations.
- Synchronize README, Quickstart, maintenance, CLI guide and the install/update Agent prompts; add regression coverage and a TL findings report.

## v1.4.1 — Compact verification and terminal self-install

- `drui verify` now prints a one-line result by default; failures list at most three details.
- Keep `drui verify --verbose` for full audit and `--json` for machine-readable output.
- Install and relink show a compact final verification instead of dozens of Skill inventory lines.
- Document direct CLI self-install from the official stable GitHub tag, with detailed setup logs kept locally.
- Require short final verification in Agent install/update prompts; tests cover summary and failure modes.

## v1.4.0 — Per-Agent Skill installation verification

- Add read-only `drui verify` and `gamekit.py verify` with per-Agent Skill name/status/path, bundled kit version and `--json` output.
- Detect missing, broken, invalid and colliding global Skill links without modifying user-owned installations.
- Include user-owned/third-party Skill inventory and declared version when available; do not fabricate independent bundled Skill versions.
- Print verification automatically after an installation or relink, while keeping dry-run strictly non-mutating.
- Clarify that a valid local link does not prove Agent runtime loading; add regression and Git-clone smoke coverage.

## v1.3.0 — GitHub source-only installation and updates

- Replaced release ZIP installer with `git clone` of the official stable GitHub Tag directly into `~/GameAgentKit`.
- Replaced ZIP SHA-256 updater with GitHub stable-release Tag discovery, official-origin validation, clean-worktree refusal and direct Git checkout. No automatic external Skill updates.
- README / QUICKSTART / clipboard Agent prompts now use GitHub source; CI and Releases no longer publish installer archives.
- No backwards compatibility for legacy ZIP-managed installations (new installation baseline).

---

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
