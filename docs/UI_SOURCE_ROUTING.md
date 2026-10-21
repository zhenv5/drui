# DRUI UI-method selection: official Pro > original Plus > open Oil UI > DRUI fallback

**Official names:** `oil-ui-pro` (paid external), `oil-ui-plus` (our original approximation, packaged here), `oil-ui` (optional external open source), `drui` (workflow orchestrator and fallback).

**Automatic priority, evaluated in the *current agent's* accessible Skill environment:**

1. Installed and accessible official `oil-ui-pro` → select it first. **Never infer that a user has purchased Pro** because the name appears in instructions or examples. Do not redistribute its content.
2. Else use packaged `oil-ui-plus` → original Pro-like guidance, not official Pro or a feature unlock. This is the normal default for a fresh installation.
3. Else use externally installed `oil-ui` → open-source UI methods.
4. Else use the built-in DRUI generic UI/UX review guidance.

Choose **one primary UI-method source**. DRUI always coordinates the 20 stages, TL/PM/User review, scorecards and evidence gates; selection does **not** replace these responsibilities. A lower-priority source may be consulted for missing, compatible guidance only if the user explicitly asks, and must be reported separately. If user specifies `--ui-source pro|plus|oil-ui|drui`, honor that exact choice or report unavailable; **never silently substitute another source**. Auto fallback on unavailability is allowed and must be disclosed. Report the selected UI-method source and whether its actual SKILL.md was read. A terminal-generated prompt reflects its environment only; confirm source availability again inside the target agent.

Examples in an Agent chat: `drui full`, `drui review-loop --ui-source plus`, `drui visual-review --ui-source oil-ui`. In a terminal, `drui sources`, `drui prompt full --ui-source plus` (prints instructions, does NOT execute).
