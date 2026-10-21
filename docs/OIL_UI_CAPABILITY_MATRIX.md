# Oil UI Plus (`oil-ui-plus`) — original approximation versus official Pro

**Important**: The user supplied a feature comparison between Oil UI open source and Oil UI Pro. The bundled **`oil-ui-plus`** Skill provides **original guidance and reference code** aiming to approximate behaviors—not official `oil-ui-pro`, its hidden prompts, paid templates, licenses, or model capabilities. Those are not included. Actual integration depends on the user's own installed Oil UI Skill.

| Feature described | In kit | Reality / limits |
|---|---|---|
| Direction + tone + comparison | `DESIGN_DIRECTIONS` | 3 distinct written concepts, compare overlap |
| Hierarchy, type, color, spacing, images, motion | `OIL_UI_ENHANCED_WORKFLOW` | checklist + code-oriented design tokens |
| Memorable moments / parallax / continuous shots | `OIL_UI_ENHANCED_WORKFLOW` | guidelines; real rendering depends on platform/tools |
| Screenshot recreation | `SCREENSHOT_TO_NATIVE` | actual image layer decomposition + rendered comparison |
| Mini-game pacing, feel, art, real-time 3D | `MINIGAME_SCENE_QA`, `REALTIME_3D_ASSET_PLAN` | state/scene acceptance; does NOT provide a 3D generator |
| Independent review and score | `OIL_UI_REVIEW_RUBRIC` | original evidence-backed scoring |
| Repeat review aiming 9/10 | `OIL_UI_ENHANCED_WORKFLOW` | up to 3 cycles; score not guaranteed |
| Check direction overlap / complete actual task | `DESIGN_DIRECTIONS` + `MINIGAME_SCENE_QA` | actual runtime required |
| Anti-AI default polish and simplification | `OIL_UI_ENHANCED_WORKFLOW` | checklist |
| Usability (states, forms, dialogs, layouts) | `COMPONENT_EXTREME_POLISH` | task + states |
| Dashboards/tools | `DASHBOARD_WORKSPACE` | workspace patterns |
| Existing project refresh / flow fix / new feature | `PROJECT_MODE_SELECTOR` | choose mode explicitly |
| Single-component extreme polish | `COMPONENT_EXTREME_POLISH` | state inventory + regression |
| 19 card prototypes with code + spatial expansion | `references/OIL_UI_19_ORIGINAL_CARD_PATTERNS.md`, `examples/OilUICardGallery.swift` | **19 original** sample designs, NOT the paid 19 |
| Light trails / dot patterns / flowing gradients | `MOTION_AND_EFFECTS`, `examples/OilUIEffectsGallery.swift` | original SwiftUI examples & performance gates |
| Mini-game scenes/visual/state checks | `MINIGAME_SCENE_QA` | full state matrix |

## The basic quality gate

For UI work: DRUI selects `oil-ui-pro` (if installed) → `oil-ui-plus` → `oil-ui` → DRUI fallback; then implement → capture actual runtime → independent review → repair → re-capture. An extension is never a substitute for visual inspection or the user's quality judgment.
