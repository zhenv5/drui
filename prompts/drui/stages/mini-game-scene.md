# Stage: mini-game-scene — 小游戏场景专项

> **UI method routing:** `oil-ui-pro` (installed and usable only) > **`oil-ui-plus`** (our original Pro-like approximation) > `oil-ui` > DRUI fallback. Honor explicit source overrides, record what was actually loaded, and never pretend Plus is official Pro.

> Purpose: Evaluate game scene layout, gameplay priority and touch controls.

## Task for the agent

Inspect actual game screen, prioritize playfield → controls → feedback → HUD. Test all game states including ready, playing, success, mistake, pause, finish. Check hand reachability, overlap, occlusion, input latency, animation timing, FPS and accessible affordances. Can be review-only unless explicit implementation requested. See prompts/drui/MINIGAME_SCENE_QA.md.

## Output contract

Name stage `mini-game-scene` and include: scope, concrete observations, affected pages/interaction states, evidence or explicitly marked BLOCKED/NOT RUN, actual changes (if stage permits), P0/P1 unresolved issues, next action. Never merge/push without user permission. Respect current app data and code. Follow `docs/UI_SOURCE_ROUTING.md`: official `oil-ui-pro` if accessible, otherwise bundled original `oil-ui-plus`, then `oil-ui`, then DRUI fallback. Disclose selected source; no paid-Pro assumptions.
