# Stage: visual-review — 独立视觉评审

> **UI method routing:** `oil-ui-pro` (installed and usable only) > **`oil-ui-plus`** (our original Pro-like approximation) > `oil-ui` > DRUI fallback. Honor explicit source overrides, record what was actually loaded, and never pretend Plus is official Pro.

> Purpose: Independently judge hierarchy, typography, spacing, materials, image integrity and coherence.

## Task for the agent

Review ACTUAL RENDERED screenshots from target simulator/browser/device at representative screens and states, not mockup pictures. Examine hierarchy, style unity, typography, text clipping, spacing, contrast, focal point, character/scene asset resolution, generic AI design defaults and unnecessary visual noise. Produce per-screen P0/P1/P2 findings, seven-axis rubric scores with screenshot evidence and concrete corrections. READ-ONLY REVIEW: do not change code in this stage. If screenshots are unavailable, status BLOCKED, no numeric visual quality pass.

## Output contract

Name stage `visual-review` and include: scope, concrete observations, affected pages/interaction states, evidence or explicitly marked BLOCKED/NOT RUN, actual changes (if stage permits), P0/P1 unresolved issues, next action. Never merge/push without user permission. Respect current app data and code. Follow `docs/UI_SOURCE_ROUTING.md`: official `oil-ui-pro` if accessible, otherwise bundled original `oil-ui-plus`, then `oil-ui`, then DRUI fallback. Disclose selected source; no paid-Pro assumptions.
