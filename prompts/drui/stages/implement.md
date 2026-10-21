# Stage: implement — 界面与交互实现

> **UI method routing:** `oil-ui-pro` (installed and usable only) > **`oil-ui-plus`** (our original Pro-like approximation) > `oil-ui` > DRUI fallback. Honor explicit source overrides, record what was actually loaded, and never pretend Plus is official Pro.

> Purpose: Implement scoped production changes in the real project.

## Task for the agent

Use the current plan and product/platform profile; implement reusable, functioning native/engine components—not baked UI screenshots. Include interaction states (pressed, disabled, loading, error, empty, completion), navigation, accessible labels, small phones and safe areas. Preserve persistent data and core logic unless explicitly changed. Run available compile/unit/static tests, and provide changed files and tests; NEVER call an unrun simulator test PASS.

## Output contract

Name stage `implement` and include: scope, concrete observations, affected pages/interaction states, evidence or explicitly marked BLOCKED/NOT RUN, actual changes (if stage permits), P0/P1 unresolved issues, next action. Never merge/push without user permission. Respect current app data and code. Follow `docs/UI_SOURCE_ROUTING.md`: official `oil-ui-pro` if accessible, otherwise bundled original `oil-ui-plus`, then `oil-ui`, then DRUI fallback. Disclose selected source; no paid-Pro assumptions.
