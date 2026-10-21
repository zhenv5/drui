# Stage: full — 完整 UI 改进循环

> **UI method routing:** `oil-ui-pro` (installed and usable only) > **`oil-ui-plus`** (our original Pro-like approximation) > `oil-ui` > DRUI fallback. Honor explicit source overrides, record what was actually loaded, and never pretend Plus is official Pro.

> Purpose: End-to-end from product intent, scope and direction through implementation, actual play, independent review, correction and proof.

## Task for the agent

Run all applicable Oil UI enhancement stages on the open project, in this order: discover → plan → implement → visual-review + usability-review (+ game-feel for games) → review-triad (TL + PM + User, isolated contexts where possible) → fix → verify. For a narrow defect omit irrelevant ideation, but keep realistic testing. Set an explicit max of three review–repair cycles; do not claim 9/10 without real screenshots and successful task reproduction. Preserve existing project design identity and functionality. Output files changed, before/after proof, screen/state coverage, honest blocked checks, and prioritized remaining issues.

## Output contract

Name stage `full` and include: scope, concrete observations, affected pages/interaction states, evidence or explicitly marked BLOCKED/NOT RUN, actual changes (if stage permits), P0/P1 unresolved issues, next action. Never merge/push without user permission. Respect current app data and code. Follow `docs/UI_SOURCE_ROUTING.md`: official `oil-ui-pro` if accessible, otherwise bundled original `oil-ui-plus`, then `oil-ui`, then DRUI fallback. Disclose selected source; no paid-Pro assumptions.

For a release-level `full` review, apply `docs/DRUI_STRICT_REVIEW_PROTOCOL.md`: the three separate reviewer reports and disagreement matrix are required. If fresh isolated contexts or device runtime are unavailable, label triad validation PROVISIONAL/BLOCKED; do not conflate a sequential role-play with three independent agent reviews.
