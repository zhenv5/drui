# Stage: fix — 按审查报告修复

> **UI method routing:** `oil-ui-pro` (installed and usable only) > **`oil-ui-plus`** (our original Pro-like approximation) > `oil-ui` > DRUI fallback. Honor explicit source overrides, record what was actually loaded, and never pretend Plus is official Pro.

> Purpose: Fix prioritized verified issues and rerun targeted checks.

## Task for the agent

Read the latest review's P0/P1 issue list and baseline captures. Fix highest-impact defects with minimal regression risk; add tests for behavior and state transitions. Rebuild, rerun affected interaction and capture fresh evidence. Do not reassign reviewer scores to yourself; independent verification comes after this stage. If no prior findings exist, request or conduct a focused review first.

## Output contract

Name stage `fix` and include: scope, concrete observations, affected pages/interaction states, evidence or explicitly marked BLOCKED/NOT RUN, actual changes (if stage permits), P0/P1 unresolved issues, next action. Never merge/push without user permission. Respect current app data and code. Follow `docs/UI_SOURCE_ROUTING.md`: official `oil-ui-pro` if accessible, otherwise bundled original `oil-ui-plus`, then `oil-ui`, then DRUI fallback. Disclose selected source; no paid-Pro assumptions.
