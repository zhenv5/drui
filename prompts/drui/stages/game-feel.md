# Stage: game-feel — 游戏手感与反馈审查

> **UI method routing:** `oil-ui-pro` (installed and usable only) > **`oil-ui-plus`** (our original Pro-like approximation) > `oil-ui` > DRUI fallback. Honor explicit source overrides, record what was actually loaded, and never pretend Plus is official Pro.

> Purpose: Review feedback latency, animation, sound, haptics and pacing.

## Task for the agent

Audit the real loop from player action to response: immediate feedback; consistent drag/tap interaction; outcome animation; micro-timing; sound and haptics; reduced-motion accessibility; no obscured playfield or excessive motion. Confirm timing and framerate on a real runtime where supported, not invented metrics. For pure review, report findings; make changes only when specifically asked to improve game feel.

## Output contract

Name stage `game-feel` and include: scope, concrete observations, affected pages/interaction states, evidence or explicitly marked BLOCKED/NOT RUN, actual changes (if stage permits), P0/P1 unresolved issues, next action. Never merge/push without user permission. Respect current app data and code. Follow `docs/UI_SOURCE_ROUTING.md`: official `oil-ui-pro` if accessible, otherwise bundled original `oil-ui-plus`, then `oil-ui`, then DRUI fallback. Disclose selected source; no paid-Pro assumptions.
