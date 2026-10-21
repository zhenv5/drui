# GameAgentKit 1.7.0 — Original Oil UI Plus with method routing

- Added a separate original `skills/oil-ui-plus/SKILL.md` (community-maintained Pro-like UI design guidance, NOT official paid Pro).
- Default UI-method priority for every DRUI stage: `oil-ui-pro` when legitimately installed > `oil-ui-plus` (bundled) > optional `oil-ui` > DRUI fallback.
- Optional user override with `--ui-source pro|plus|oil-ui|drui` or auto; a forced unavailable source fails instead of silently falling back.
- Added `drui sources`, `drui plus`, `drui pro`, and `drui prompt <stage> --ui-source plus`; stage and independent reviewer prompts declare the priority.
- Full 20-workflow DRUI orchestrator unchanged; added provenance reporting and detection of installed UI-method Skills.
- No Oil UI Pro subscription, proprietary code, or assets are bundled.
- Includes cross-agent source-scoping and regression tests.
