# Stage: component-polish — 单组件极致打磨

> **UI method routing:** `oil-ui-pro` (installed and usable only) > **`oil-ui-plus`** (our original Pro-like approximation) > `oil-ui` > DRUI fallback. Honor explicit source overrides, record what was actually loaded, and never pretend Plus is official Pro.

> Purpose: Polish one component and every interactive and content state.

## Task for the agent

Select the named component and enumerate default/pressed/selected/loading/disabled/error/long-copy/dynamic-type/small-device states. Improve legibility, hit target, focus behavior, transition motion, design-system fit and code reuse. Implement only this component, exercise it live and document before/after. See prompts/drui/COMPONENT_EXTREME_POLISH.md.

## Output contract

Name stage `component-polish` and include: scope, concrete observations, affected pages/interaction states, evidence or explicitly marked BLOCKED/NOT RUN, actual changes (if stage permits), P0/P1 unresolved issues, next action. Never merge/push without user permission. Respect current app data and code. Follow `docs/UI_SOURCE_ROUTING.md`: official `oil-ui-pro` if accessible, otherwise bundled original `oil-ui-plus`, then `oil-ui`, then DRUI fallback. Disclose selected source; no paid-Pro assumptions.
