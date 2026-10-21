# Stage: dashboard — 仪表盘 / 工具页专项

> **UI method routing:** `oil-ui-pro` (installed and usable only) > **`oil-ui-plus`** (our original Pro-like approximation) > `oil-ui` > DRUI fallback. Honor explicit source overrides, record what was actually loaded, and never pretend Plus is official Pro.

> Purpose: Audit workspace IA, filters, empty/loading/error states and action completion.

## Task for the agent

Choose a product-appropriate information architecture, check task hierarchy, filter semantics, list/table/card density, consistency, responsive layout, clear primary action, keyboard/mobile interaction and data states. If requested to build, implement and test. See prompts/drui/DASHBOARD_WORKSPACE.md.

## Output contract

Name stage `dashboard` and include: scope, concrete observations, affected pages/interaction states, evidence or explicitly marked BLOCKED/NOT RUN, actual changes (if stage permits), P0/P1 unresolved issues, next action. Never merge/push without user permission. Respect current app data and code. Follow `docs/UI_SOURCE_ROUTING.md`: official `oil-ui-pro` if accessible, otherwise bundled original `oil-ui-plus`, then `oil-ui`, then DRUI fallback. Disclose selected source; no paid-Pro assumptions.
