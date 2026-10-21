# Stage: plan — 设计方向 / 改造计划

> **UI method routing:** `oil-ui-pro` (installed and usable only) > **`oil-ui-plus`** (our original Pro-like approximation) > `oil-ui` > DRUI fallback. Honor explicit source overrides, record what was actually loaded, and never pretend Plus is official Pro.

> Purpose: Plan distinct directions and a design system matched to the actual product.

## Task for the agent

For a substantial redesign, compare three structurally distinct directions on layout, hierarchy, focus, typography, color roles, illustration/materials and interactions; reject near-duplicate recolors and choose one with reasoning. For a flow fix, give a minimum-diff task journey plan instead; for a component fix, stay in scope. Define reusable tokens and screen/state matrix, dependencies, accessibility/reduced motion and evidence needed. This stage plans; do not claim implementation or testing.

## Output contract

Name stage `plan` and include: scope, concrete observations, affected pages/interaction states, evidence or explicitly marked BLOCKED/NOT RUN, actual changes (if stage permits), P0/P1 unresolved issues, next action. Never merge/push without user permission. Respect current app data and code. Follow `docs/UI_SOURCE_ROUTING.md`: official `oil-ui-pro` if accessible, otherwise bundled original `oil-ui-plus`, then `oil-ui`, then DRUI fallback. Disclose selected source; no paid-Pro assumptions.
