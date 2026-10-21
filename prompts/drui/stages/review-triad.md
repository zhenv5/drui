# Stage: review-triad — TL + PM + User 严苛三方独立审查

> **UI method routing:** `oil-ui-pro` (installed and usable only) > **`oil-ui-plus`** (our original Pro-like approximation) > `oil-ui` > DRUI fallback. Honor explicit source overrides, record what was actually loaded, and never pretend Plus is official Pro.

> Review-only orchestration. Do not modify any product source or pretend to run three genuinely isolated agents in one chat.

## Task for the agent

1. Run `python3 ~/GameAgentKit/gamekit.py review prepare --project "$PWD" --output ./drui-reviews/<run-id>` (choose a unique run-id; ask for authorization if writing outside allowed workspace).
2. Assign generated `PROMPT_tech-lead.md`, `PROMPT_product-manager.md`, `PROMPT_end-user.md` to three **fresh independent agent contexts**. Do not give a reviewer another's findings before it has filed its report. If multi-agent delegation unavailable, run three sequential reviewer lenses marked `single-session` and call the result **PROVISIONAL**.
3. Each reviewer must inspect the same baseline build and actual workflows, separately record evidence, failing steps, five-axis 0–10 scores, P0/P1/P2/P3 and the requested JSON.
4. Only after all 3 completed reports: compare overlapping findings, conflicting findings, missing/unsupported claims, and changes PM wants that engineering rejects. Resolve conflicts using replayable proof or mark unresolved. No majority vote to waive a P0.
5. Run `python3 ~/GameAgentKit/gamekit.py review evaluate --dir ./drui-reviews/<run-id>` and include its complete gate result. It checks report completeness and file presence, not authenticity of evidence.

## Output contract

Three isolated role reports + an adjudication matrix: finding / role / evidence / disposition / rationale / owner / acceptance test. No edits to source. Show lowest axis and lowest role score; **all three must individually reach >=9, every axis >=8, zero unresolved P0/P1 and real evidence** to recommend release. If incomplete, label BLOCKED/PROVISIONAL/NOT APPROVED.

If any real runtime, independent reviewer context, screenshot or essential task evidence is absent, mark that check `NOT RUN / BLOCKED` and do not certify a 9/10 release.
