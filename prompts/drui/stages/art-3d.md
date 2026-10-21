# Stage: art-3d — 角色 / 3D 资产专项

> **UI method routing:** `oil-ui-pro` (installed and usable only) > **`oil-ui-plus`** (our original Pro-like approximation) > `oil-ui` > DRUI fallback. Honor explicit source overrides, record what was actually loaded, and never pretend Plus is official Pro.

> Purpose: Plan or QA art assets for standalone production use.

## Task for the agent

Set explicit deliverable contracts: separate transparent PNG/GLB per actor, no UI/text or collage, source detail and origin, pose identity, material/light consistency, licensing, mobile performance and game import. Reject faked upscales and unapproved assets. MCP/art model access is external and optional; never claim generated assets without files. See prompts/drui/REALTIME_3D_ASSET_PLAN.md.

## Output contract

Name stage `art-3d` and include: scope, concrete observations, affected pages/interaction states, evidence or explicitly marked BLOCKED/NOT RUN, actual changes (if stage permits), P0/P1 unresolved issues, next action. Never merge/push without user permission. Respect current app data and code. Follow `docs/UI_SOURCE_ROUTING.md`: official `oil-ui-pro` if accessible, otherwise bundled original `oil-ui-plus`, then `oil-ui`, then DRUI fallback. Disclose selected source; no paid-Pro assumptions.
