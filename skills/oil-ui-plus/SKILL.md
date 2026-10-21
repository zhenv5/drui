---
name: oil-ui-plus
description: Original, community-maintained Pro-like UI design and review guidance bundled with GameAgentKit. Offers design-direction comparison, UI/UX and screenshot QA, iterative scored review, component polish, mobile and game scene checks, and sample SwiftUI cards/effects. This is NOT the official paid oil-ui-pro skill.
---

# Oil UI Plus — original DRUI-enhanced UI methods

**Source identity:** `oil-ui-plus` is the original, open implementation bundled with GameAgentKit. It is **not** `oil-ui-pro`, does not unlock paid functionality, and contains no copied proprietary assets, templates or prompts. It may be used without an Oil UI account. See `docs/OIL_UI_CAPABILITY_MATRIX.md` for precise limits.

## Source selection, always first

DRUI selects **one primary UI-method skill per task** using the order:

1. `oil-ui-pro` — official paid skill, **only if actually installed and usable by the current agent**.
2. `oil-ui-plus` — this bundled original Pro-like approximation (if available).
3. `oil-ui` — independently installed open-source Oil UI skill (if available).
4. `drui` native patterns — fallback when none of the above can be accessed.

**Do not load a lower priority source in place of an available higher one unless the user explicitly requests it.** DRUI remains the workflow **orchestrator** (stage selection, three-role review, evidence gates and QA) regardless of source. Report `requested_source`, `selected_source`, `skill_path_or_identifier`, `access_verification`, and `fallback_reason` (if any). A filename alone is not evidence of paid entitlement. A tool may legitimately be unavailable; report it instead of claiming Pro executed.

## What Oil UI Plus actually provides (original guidance)

1. Design mode decision: UI refresh vs flow repair vs new feature; compare 2–3 genuinely different directions when appropriate.
2. Visual art direction: typographic hierarchy, tonal palette, spacing, imagery, context-aware layout and purposeful motion.
3. Anti-template audit: identify stock dashboard grids, purposeless gradients/shadows, generic icons, repetition and oversaturated effects; simplify.
4. Screenshot-to-native rebuild: measure layout/typography/color, implement real accessible widgets and dynamic content, compare screenshots at matched viewports.
5. Interaction-state QA: tap/drag, hover/focus where relevant, loading/disabled/error/empty/long-text, dialogs, reachability, responsiveness, accessibility and reduced motion.
6. Component craftsmanship: explore all component states, extreme micro-polish, 19 **original** card patterns plus functional SwiftUI examples.
7. Visual effects and storytelling: optional parallax, light trails, dot patterns, flowing gradients and transitions with performance and accessibility budgets.
8. Mini-game scenes: readable playfield, touch input, HUD, feedback timing, pause/win/lose states; 3D scene and generated asset acceptance guidance (no automatic 3D service).
9. Dashboard/tool layouts: fit information architecture to product workflows rather than copying generic templates.
10. Strict independent review: evidence-backed seven-axis rubric, reproducible user task, prioritized P0/P1/P2, maximum three useful review/fix cycles toward 9/10.

## Documents to read on demand (root-relative paths)

- `prompts/OIL_UI_ENHANCED_WORKFLOW.md` — primary original UI workflow.
- `prompts/drui/PROJECT_MODE_SELECTOR.md`, `DESIGN_DIRECTIONS.md`, `SCREENSHOT_TO_NATIVE.md`, `COMPONENT_EXTREME_POLISH.md` — focused methods.
- `prompts/drui/MINIGAME_SCENE_QA.md`, `MOTION_AND_EFFECTS.md`, `DASHBOARD_WORKSPACE.md`, `REALTIME_3D_ASSET_PLAN.md` — specialized guidance.
- `docs/OIL_UI_CAPABILITY_MATRIX.md` and `docs/OIL_UI_REVIEW_RUBRIC.md` — limits and scoring.
- `references/OIL_UI_19_ORIGINAL_CARD_PATTERNS.md`, `examples/OilUICardGallery.swift`, `examples/OilUIEffectsGallery.swift` — original examples, not official paid components.

## Invocation examples

- `Use drui full. Select the best available UI source automatically.`
- `Use drui visual-review --ui-source plus. Run Oil UI Plus only; read-only.`
- `Use drui review-loop --ui-source plus. Apply original Oil UI Plus rubric with independent TL/PM/User reviews.`

**Execution rule:** A prompt generator or CLI does NOT run the review; agent execution requires real code, UI runtime and relevant tools. If actual screenshots, separated reviewer contexts or user-task execution are missing, mark them `BLOCKED` / `PROVISIONAL`. Never award an unsupported 9/10.

## Stability contract

Our original Oil UI Plus is bundled and versioned with GameAgentKit. If an optional open-source or paid external Oil UI Skill upgrades unexpectedly, run `drui deps check` and prefer this bundled Plus until the external Skill has been independently re-reviewed and approved. Never impersonate official Pro.
