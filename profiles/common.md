## Universal project expectations

- Read the repository's existing architecture, README, gameplay rules and licensing before changing anything.
- Treat real in-game screenshots as the final visual benchmark, not concept compositions.
- Preserve gameplay correctness, data, accessibility and platform conventions.
- Carry out independent player, visual/design, and technical QA cycles after code changes.
- Record all assumptions; do not invent build passes or quality ratings.
- Do not introduce a server, subscription, tracking, app account, monetization or multiplayer without a project requirement.
- Prefer small reversible changes; do not push to main unless explicitly authorized.

## Project-specific notes to fill in

Audience: [set this for the game]
Primary interaction: [touch / drag / keyboard / controller]
Core loop: [one sentence]
Art target: [reference files, if any]
Platforms and orientations: [target devices]


## Oil UI design QA (shared across games)

When creating/modifying UI: invoke optional installed `oil-ui`, then shared `drui`. Choose Refresh / Flow Fix / New Feature / Component / Mini-Game scene; use screenshot + real task + scored review and repeat up to three times. See `prompts/OIL_UI_ENHANCED_WORKFLOW.md`. This kit's prompts are original approximations of described Pro workflows, not Pro templates or a Pro license.
