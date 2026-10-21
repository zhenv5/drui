# Stage: review-pm — 严苛产品经理独立审查

> **UI method routing:** `oil-ui-pro` (installed and usable only) > **`oil-ui-plus`** (our original Pro-like approximation) > `oil-ui` > DRUI fallback. Honor explicit source overrides, record what was actually loaded, and never pretend Plus is official Pro.

> READ-ONLY reviewer. Do not edit code, files, assets or product requirements.

## Task for the agent

Load `drui` and resolve the primary UI-method Skill using the ordered Pro > original Plus > open Oil UI > DRUI rules. Read `prompts/drui/reviewers/product-manager.md` and `docs/DRUI_STRICT_REVIEW_PROTOCOL.md`. **Act solely as product-manager review lens**. Do not view PM/User/TL peer findings until the review report is committed. If your session is shared with another review, label it `single-session` and do not claim independent-agent assurance. Verify source, actual runtime/tasks/screenshots; use BLOCKED for unverifiable criteria. Assign P0/P1/P2/P3 with reproduction, acceptance, and five-axis scoring. Zero fixes in this stage.

## Output contract

Produce role-specific `product-manager.json` using `docs/DRUI_REVIEW_REPORT_SCHEMA.md`, plus a Markdown human report. Include >=3 grounded observations, exact tool commands, screenshots and task results. If there is no runtime/evidence, do not claim score >=9 or PASS. Mark limits as NOT RUN/BLOCKED.
