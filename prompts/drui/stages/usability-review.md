# Stage: usability-review — 独立 UX / 操作性评审

> **UI method routing:** `oil-ui-pro` (installed and usable only) > **`oil-ui-plus`** (our original Pro-like approximation) > `oil-ui` > DRUI fallback. Honor explicit source overrides, record what was actually loaded, and never pretend Plus is official Pro.

> Purpose: Reproduce the real primary user task and error paths.

## Task for the agent

Start the actual app and complete one real target task using device-appropriate tap, drag, swipe or keyboard. Examine discoverability, targets, safe areas, disabled/error/loading, dialogs, popovers, re-entry, pauses and accidental input. Record steps, screenshots, expected vs actual behavior, fail points and prioritized fixes. READ-ONLY REVIEW; no changes. If runtime unavailable report NOT RUN/BLOCKED and list reproducible steps for a Mac-based agent to execute.

## Output contract

Name stage `usability-review` and include: scope, concrete observations, affected pages/interaction states, evidence or explicitly marked BLOCKED/NOT RUN, actual changes (if stage permits), P0/P1 unresolved issues, next action. Never merge/push without user permission. Respect current app data and code. Follow `docs/UI_SOURCE_ROUTING.md`: official `oil-ui-pro` if accessible, otherwise bundled original `oil-ui-plus`, then `oil-ui`, then DRUI fallback. Disclose selected source; no paid-Pro assumptions.
