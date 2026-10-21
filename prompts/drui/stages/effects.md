# Stage: effects — 动效 / 光效专项

> **UI method routing:** `oil-ui-pro` (installed and usable only) > **`oil-ui-plus`** (our original Pro-like approximation) > `oil-ui` > DRUI fallback. Honor explicit source overrides, record what was actually loaded, and never pretend Plus is official Pro.

> Purpose: Review or implement purposeful motion and graphical effects.

## Task for the agent

Choose one justified animation or effect; validate hierarchy, clarity, performance, reduced motion, frame budget and no interruption to input. Avoid ornamental glowing gradients and distracting parallax. If asked to implement, use platform-native primitives and test target devices. See prompts/drui/MOTION_AND_EFFECTS.md and examples/OilUIEffectsGallery.swift.

## Output contract

Name stage `effects` and include: scope, concrete observations, affected pages/interaction states, evidence or explicitly marked BLOCKED/NOT RUN, actual changes (if stage permits), P0/P1 unresolved issues, next action. Never merge/push without user permission. Respect current app data and code. Follow `docs/UI_SOURCE_ROUTING.md`: official `oil-ui-pro` if accessible, otherwise bundled original `oil-ui-plus`, then `oil-ui`, then DRUI fallback. Disclose selected source; no paid-Pro assumptions.
