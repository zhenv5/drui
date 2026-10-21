---
name: drui
description: Cross-agent UI design and UI quality Skill. If asked "drui list", show all 20 workflow names and uses without modifying the project. Activate for UI audits, redesign, screenshot recreation, UX, game HUD/scenes, animations, strict Tech Lead/PM/User reviews, or quality loops. Supports independent stage commands, strict Tech Lead / PM / User reviewer gates, and review/fix/verify loops. UI-method selection: installed official oil-ui-pro > bundled original oil-ui-plus > optional oil-ui > DRUI fallback; never claim paid Pro without actual access.
---

# DRUI — independent UI design & quality workflow

DRUI is the **orchestrator**. The original, bundled Pro-like UI layer is now named **Oil UI Plus** (`oil-ui-plus`), an actual separate Skill. It is NOT the official paid `oil-ui-pro`, does not unlock it, and bundles no proprietary prompts or templates. The existing open `oil-ui` Skill remains external and optional.

**MANDATORY method-selection priority (for every DRUI stage):**

1. `oil-ui-pro` — use only when the OFFICIAL paid Skill is installed and accessible to the current Agent.
2. `oil-ui-plus` — our original Pro-like guidance, bundled here; use by default when Pro unavailable.
3. `oil-ui` — external open source, if installed; use when higher options unavailable or explicitly selected.
4. `drui` — generic in-kit fallback when above unavailable.

Pick one PRIMARY UI method. **Never silently claim Pro or confuse Plus with Pro.** Recheck the selected SKILL.md from the target Agent, record `requested_source`, `selected_source`, `actual_skill_read` and `fallback_reason`. User overrides such as `drui full --ui-source plus` take precedence; if the requested source is missing, stop and report it rather than auto-downgrade. Generic DRUI workflow and independent reviewer gates always apply, regardless of method. See `docs/UI_SOURCE_ROUTING.md`.

## External Skill upgrade & compatibility guard (V1.8)

- `drui update` updates ONLY the GameAgentKit release. It NEVER updates `oil-ui-pro`, `oil-ui` or any third-party Skill.
- `drui deps list` enumerates installed external Skills; `drui deps lock` records the initial file hashes; `drui deps check` detects additions, removals, or changed contents; `drui deps approve --name <skill> --evidence REVIEW.md` accepts a new fingerprint ONLY after independent compatibility review.
- If a dependency lock exists, an unapproved or changed external UI Skill must be excluded from automatic UI source selection. Preserve priority `oil-ui-pro` > **our original `oil-ui-plus`** > open-source `oil-ui` > DRUI fallback, but skip any unapproved external Skill. Do not auto-upgrade, auto-approve, or pretend the new version passed.
- An explicit `--ui-source pro` or `--ui-source oil-ui` request must STOP when the installed version is unapproved; never silently downgrade. `--ui-source plus` remains available independently.
- If no dependency lock exists, report **UNLOCKED / NOT VERIFIED** and recommend creating one; detecting a valid file or SHA-256 does NOT establish runtime compatibility.
- External Skills can change their instructions, required tools, APIs and security behavior. Review the diff, permissions, tool calls, licenses and run isolated practical tasks before approving. Content fingerprints detect change but cannot prove safety.

Read, in order:
1. The project's README, product constraints and any `.game-agent-kit/PROFILE.md`.
2. Read the chosen PRIMARY UI-method Skill according to priority above (`oil-ui-pro`, `oil-ui-plus`, `oil-ui`, or DRUI itself); do not read or modify a paid Skill that is not installed.
3. For `oil-ui-plus`, read `~/GameAgentKit/prompts/OIL_UI_ENHANCED_WORKFLOW.md` (or kit-local equivalent), plus mode-specific prompts under `prompts/drui/`; if Pro selected its own licensed instructions govern the UI methods.
4. `~/GameAgentKit/docs/OIL_UI_CAPABILITY_MATRIX.md` and `docs/OIL_UI_REVIEW_RUBRIC.md`.

## Decide the work type before modifying UI

- **UI refresh**: the flow is sound but the visuals underperform; preserve screen navigation, game rules and key controls.
- **Flow fix**: players cannot find or finish the task; fix the journey and states first, then polish.
- **New feature**: add a small end-to-end vertical slice that matches existing product identity.
- **Component deep dive**: polish one component's every state, interaction, content variation and breakpoint.
- **Mini-game scene**: playfield > controls > feedback > pause/end; preserve input legibility and frame budget.

## DRUI command router — `drui list` (V1.5)

**Interpret direct chat invocations** as DRUI requests when this Skill is installed:

- `drui` or `drui list` → **display the complete workflow menu** from `docs/DRUI_COMMANDS_ZH.md` or run `python3 ~/GameAgentKit/scripts/drui list` if a terminal is available. No project edits. Include each name, a one-line purpose, and the distinction between read-only and edit-capable stages. **Do not start `full`** simply because the user asked for a list.
- `drui help <stage>` / `drui show <stage>` → explain that workflow, its scope, read/write permissions, intended evidence and how to trigger it. No project changes.
- `drui <stage> [--ui-source auto|pro|plus|oil-ui|drui]` or `drui run <stage>` in **agent chat** → read `prompts/drui/stages/<stage>.md`, follow the chosen stage on the open project. Do not broaden scope. Ask for any truly required target details if missing.
- `drui sources` → show UI methods, priority and pinned dependency status; read-only.
- `drui deps list|conflicts|lock|check|approve` → external Skill inventory, local fingerprint baseline, drift detection and explicitly reviewed update approval; does NOT update external packages.
- `drui plus` / `drui pro` in agent chat → run `full` forcing the Plus or actual installed Pro method respectively. No silent fallback for forced Pro.
- `drui prompt <stage>` in **agent chat** → display the ready-to-copy instructions only; do not start work.
- Unknown stage → show valid names using `drui list`, do not silently choose a different workflow.

**Terminal semantics differ:** `drui list`, `drui help <stage>` and `drui prompt <stage>` are read-only output commands; even `drui review-tl` on a terminal only PRINTS a prompt and never launches an agent. To actually execute a workflow, request it in an Agent conversation (with necessary tools) or paste the printed prompt into that conversation. The CLI is installed at `~/.local/bin/drui` by `install.sh` / `gamekit.py link`; if outside shell PATH, run `python3 ~/GameAgentKit/scripts/drui list`, or add `~/.local/bin` to PATH manually. Never change PATH automatically.

The menu has 20 workflows grouped as:
- **核心开发:** `full`, `discover`, `plan`, `implement`, `fix`, `verify`.
- **界面与体验:** `visual-review`, `usability-review`, `game-feel`, `screenshot-rebuild`, `component-polish`.
- **专项设计:** `mini-game-scene`, `effects`, `dashboard`, `art-3d`.
- **严苛三方评审:** `review-tl`, `review-pm`, `review-user`, `review-triad`, `review-loop`.

`review-triad` requires truly isolated review contexts for independent approval; otherwise mark PROVISIONAL. `review-loop` can edit implementation after review. All other `review-*` stages are strictly read-only.

## Name / how to trigger / independent stage rules

Official, portable orchestrator Skill name: `drui` (separate from original `oil-ui-plus`, optional external `oil-ui`, and optional paid `oil-ui-pro`).

An agent may discover this Skill automatically for UI-design/review requests, **but automatic activation varies by agent and is not guaranteed**. To trigger reliably, explicitly say `Use the drui skill` and name the stage. Slash syntax such as `/drui` may be available in some agents but is **not universal**; do not rely on it.

Examples of direct commands:
- `Use drui. Stage: full. Review, implement, test and iterate the open game's UI.`
- `Use drui. Stage: visual-review. Report only, do not edit files.`
- `Use drui. Stage: usability-review. Actually complete the main touch task.`
- `Use drui. Stage: component-polish. Polish only the pause button.`
- `Use drui. Stage: fix. Use prior review findings and test changes.`

Independently runnable stages are defined under `~/GameAgentKit/prompts/drui/stages/<stage>.md`; use `python3 ~/GameAgentKit/gamekit.py workflow list` to enumerate, and `python3 ~/GameAgentKit/gamekit.py workflow prompt --stage visual-review` to print a ready-to-paste prompt. The CLI **prints instructions**; it does not invoke an agent or perform review/implementation by itself.

**Stage contracts:** `discover`, `plan`, `visual-review`, `usability-review`, and `verify` are analysis/review stages and must not silently change code. `implement`, `fix`, `screenshot-rebuild` and `component-polish` can change code if explicitly requested. Other specialist stages may review only or implement according to the request. **All `review-*` reviewer stages except `review-loop` are strictly read-only.** `full` orchestrates the applicable stages. Absence of a runtime blocks visually scored approval.

## Strict, isolated reviewer workflows (V1.4)

- `review-tl` — **Tech Lead** technical correctness, architecture, performance, risks (READ-ONLY).
- `review-pm` — **Product Manager** user value, onboarding, progression, scope, release readiness (READ-ONLY).
- `review-user` — **User lens** complete actual user task without developer hints, confusion/recovery/accessibility (READ-ONLY).
- `review-triad` — generate separate assignments with `gamekit.py review prepare`, gather all 3 reports from isolated agent contexts, independently score, adjudicate conflicts (READ-ONLY).
- `review-loop` — triad review, separate implementation fixes, real re-test and fresh reviewer re-evaluation (max 3 iterations; implementation permitted after initial reports).

See `docs/DRUI_STRICT_REVIEW_PROTOCOL.md`, `docs/DRUI_REVIEW_REPORT_SCHEMA.md`, `prompts/drui/reviewers/`. **Never claim three independent agents were used when it was one model in a single shared context.** In that fallback mark `PROVISIONAL`. No real app runtime ⇒ screenshots/UX evidence `BLOCKED`, never 9/10 release PASS. Reviewers must not change code; an implementer must not change reviewer reports. P0/P1 findings remain release blockers regardless of average score. The deterministic `review evaluate --dir` command validates report completeness and evidence file presence, not truth of content or independence.

## Required sequence

A. Inspect real UI and choose two or three intentionally distinct design directions when exploring a new direction. Compare by compositional structure, accent roles, typography and interaction emphasis, not just recoloring. Pick one on product fit.

B. Establish a design system and implement real, reusable components; preserve math/text/data as dynamic app state. Prefer native/mobile interactions over decorative flourishes. Use assets only with explicit readiness metadata and transparent/background requirements.

C. Run independent visual review on **actual rendered screenshots** and complete at least one *real user task* in the target app. Inspect tap/drag, disabled/loading/error/empty/long-text, dialogs/popovers, safe areas, small phones/tablets, accessibility and reduced motion where applicable.

D. Score with `OIL_UI_REVIEW_RUBRIC.md` and log **findings → fixes → re-render → new findings**. Aim for >=9.0/10, but do not claim success unless supported by evidence; report BLOCKED/NOT RUN truthfully. Do not endlessly optimize against self-awarded scores; stop after up to 3 useful cycles and list remaining risks.

E. Check for common AI defaults (generic cards, purposeless gradients, random shadows, stock icons, repetitive panels) and simplify before adding effects. Where justified use depth, subtle parallax, continuous-shot transitions, guided moments or small shader effects without obscuring gameplay, accessibility, or performance.

## Optional original pattern library

Oil UI Plus includes **19 original card patterns**, with interaction and responsive examples, under `references/OIL_UI_19_ORIGINAL_CARD_PATTERNS.md` and `examples/OilUICardGallery.swift`; sample effects are in `examples/OilUIEffectsGallery.swift`. This does **not** include any paid Oil UI Pro templates or assets.

## Reporting contract

Supply: mode, primary user task, chosen direction + rejected alternatives, affected screens, code/asset diffs, before/after *real* captures, reproducible user-task results, 0–10 axis scoring with evidence, unresolved P0/P1, and exact next action. If no UI runtime is available: Visual QA = BLOCKED, not PASS.

## Duplicate and user-managed Skills
If users install their own Skills (including the same name as one provided by GameAgentKit), **never overwrite, auto-remove, auto-downgrade or silently relink them**. First run `drui deps conflicts --project <repo>` and `drui deps check` (if baseline exists), identify exact paths and hashes, and disclose ambiguity about the actual Skill loaded. A user-upgraded same-name skill is an unmanaged external dependency, not an automatic kit upgrade. Preserve external files and require a review before marking new content compatible. The project or Agent might use a different copy; verify its actual SKILL.md path.
