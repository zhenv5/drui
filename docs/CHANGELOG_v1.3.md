> ARCHIVED **internal GameAgentKit** milestone. These historical V1.x labels are not the current public DRUI Release version. For current GitHub-only installation see [Install & Verify](INSTALL_AND_VERIFY.md).

# V1.3 — DRUI

- Rename only the GameAgentKit UI review Skill from `oil-ui-enhanced-review` to `drui`; never rename external `oil-ui`.
- Single global Skill `skills/drui/SKILL.md`, 15 independent stage prompts under `prompts/drui/stages`.
- CLI `workflow list`, `workflow prompt --stage ...` now activates `drui`.
- `migrate-drui` safely archives legacy Skill and removes only its confirmed owned global links; optional per-project managed rules can be refreshed with backups.
- `extend-oil-ui --refresh` opt-in backs up/refreshes only the managed external `oil-ui` extension, not its original content.
- Updated README, QUICKSTART and DRUI_USAGE with all installation/migration/trigger commands and stages.
- Tests cover new name, all 15 stages, dry-run, migration idempotency, collision safety, project block refresh and optional external extension refresh.
