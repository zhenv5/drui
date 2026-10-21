# Universal 3-pass game polish prompt

Act as a new player, game UI/art director and senior engineer independently. Use the globally installed `game-qa-review`, `game-ui-design`, `game-ux-flow`, `game-feel-polish`, and `drui` skills. If the owner has `oil-ui` installed, invoke it at each UI gate; never assume Pro capabilities. Read the current game's README and `.game-agent-kit/PROFILE.md` if present. Preserve existing gameplay rules, assets and architecture unless changes are justified.

Pass 1 — User: play actual game from a cold start; identify confusing input, touch accuracy, navigation, pause, retries and progression. Fix P0/P1 and test.
Pass 2 — Art/UX: capture actual device/browser screenshots; compare to reference art and design system, fix spacing/contrast/responsive layout/visual coherence without baking UI into screenshots. Test again.
Pass 3 — Technical: cover state races, timers, audio, lifecycle, persistence, regression tests, performance and reduced-motion. Fix and repeat smoke test.

For each pass provide: findings ranked by impact, exact files changed, commands/logs actually run, device/screenshots when available and remaining issues. If no real device/simulator/browser, say BLOCKED rather than inventing results. Never merge or push without approval.

### Oil UI inspection gates (required for UI tasks)

- **Before coding:** use installed `oil-ui` + `drui` to choose Refresh/Flow Fix/Feature/Component/Scene; compare visual directions only for broad redesign.
- **After first render:** independently inspect real screenshot, states and one completed user task; apply `docs/OIL_UI_REVIEW_RUBRIC.md`, write score + concrete findings.
- **After fixing:** rerender and review again, up to 3 loops targeting 9/10 (not guaranteed); never call an unavailable plugin, mock screenshot or unexecuted task PASS.

Paste `prompts/OIL_UI_ENHANCED_WORKFLOW.md` for detailed prompts that approximate *categories* of paid features using entirely original instructions and code examples.
