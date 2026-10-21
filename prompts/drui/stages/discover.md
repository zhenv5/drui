# Stage: discover — 现状诊断 / 问题分类

> **UI method routing:** `oil-ui-pro` (installed and usable only) > **`oil-ui-plus`** (our original Pro-like approximation) > `oil-ui` > DRUI fallback. Honor explicit source overrides, record what was actually loaded, and never pretend Plus is official Pro.

> Purpose: Inspect project goals, screens, navigation, reference images, code and runtime evidence before changing anything.

## Task for the agent

Read the game/product spec and optional .game-agent-kit/PROFILE.md; inspect the real code and existing images/screens if available. Identify platform, audience, game loop, essential task, touch/drag constraints and runtime environment. Classify the requested work as visual refresh, flow fix, new feature, component polish or mini-game scene. Produce a scope map, P0/P1 issues and a baseline evidence checklist. This stage is ANALYSIS ONLY; do not alter source or infer visual quality from source code.

## Output contract

Name stage `discover` and include: scope, concrete observations, affected pages/interaction states, evidence or explicitly marked BLOCKED/NOT RUN, actual changes (if stage permits), P0/P1 unresolved issues, next action. Never merge/push without user permission. Respect current app data and code. Follow `docs/UI_SOURCE_ROUTING.md`: official `oil-ui-pro` if accessible, otherwise bundled original `oil-ui-plus`, then `oil-ui`, then DRUI fallback. Disclose selected source; no paid-Pro assumptions.
