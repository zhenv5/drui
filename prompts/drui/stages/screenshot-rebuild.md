# Stage: screenshot-rebuild — 参考截图还原

> **UI method routing:** `oil-ui-pro` (installed and usable only) > **`oil-ui-plus`** (our original Pro-like approximation) > `oil-ui` > DRUI fallback. Honor explicit source overrides, record what was actually loaded, and never pretend Plus is official Pro.

> Purpose: Translate a screenshot into real responsive application UI.

## Task for the agent

Use the original screenshot as visual reference, separate backdrop, imagery, typographic content, controls and dynamic state. Rebuild with real components and accessible hit regions; compare matching screen sizes with actual rendered output using side-by-side QA. Do not crop a promotional board into an app screen and call it implemented. Use prompts/drui/SCREENSHOT_TO_NATIVE.md for details.

## Output contract

Name stage `screenshot-rebuild` and include: scope, concrete observations, affected pages/interaction states, evidence or explicitly marked BLOCKED/NOT RUN, actual changes (if stage permits), P0/P1 unresolved issues, next action. Never merge/push without user permission. Respect current app data and code. Follow `docs/UI_SOURCE_ROUTING.md`: official `oil-ui-pro` if accessible, otherwise bundled original `oil-ui-plus`, then `oil-ui`, then DRUI fallback. Disclose selected source; no paid-Pro assumptions.
