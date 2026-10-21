# Stage: verify — 回归验收与评分

> **UI method routing:** `oil-ui-pro` (installed and usable only) > **`oil-ui-plus`** (our original Pro-like approximation) > `oil-ui` > DRUI fallback. Honor explicit source overrides, record what was actually loaded, and never pretend Plus is official Pro.

> Purpose: Independent final QA after fixes with evidence and truthful score.

## Task for the agent

Build/run target game, complete at least one full primary task, test all modified screens/states and regression-critical paths, capture after screenshots with target device and sizes, and compare to baseline. Independently score seven axes against docs/OIL_UI_REVIEW_RUBRIC.md. Target 9/10 but never fabricate numbers or claim Pro-specific tools. Output PASS/FAIL/BLOCKED/NOT RUN by check, remaining P0/P1, and a stop/iterate decision (max 3 useful cycles). This stage does not implement fixes.

## Output contract

Name stage `verify` and include: scope, concrete observations, affected pages/interaction states, evidence or explicitly marked BLOCKED/NOT RUN, actual changes (if stage permits), P0/P1 unresolved issues, next action. Never merge/push without user permission. Respect current app data and code. Follow `docs/UI_SOURCE_ROUTING.md`: official `oil-ui-pro` if accessible, otherwise bundled original `oil-ui-plus`, then `oil-ui`, then DRUI fallback. Disclose selected source; no paid-Pro assumptions.
