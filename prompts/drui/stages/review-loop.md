# Stage: review-loop — 严苛三方审查→修复→复审闭环

> **UI method routing:** `oil-ui-pro` (installed and usable only) > **`oil-ui-plus`** (our original Pro-like approximation) > `oil-ui` > DRUI fallback. Honor explicit source overrides, record what was actually loaded, and never pretend Plus is official Pro.

> This is the only new reviewer-focused stage that can modify implementation, *after* collecting independent READ-ONLY reviews.

## Task for the agent

1. Save a baseline git revision and product invariants. Use `review-triad` to collect 3 separately isolated reviewer reports on the same build. Choose primary UI method with priority oil-ui-pro > oil-ui-plus > oil-ui > DRUI; respect explicit override and log actual access.
2. Synthesize a prioritized backlog: P0 blocks all polish, P1 must be resolved before approval, P2 cosmetic improvements after functional fixes; preserve conflicts with reviewer evidence.
3. Open a SEPARATE implementation context to fix issues one at a time. Add reproducible automated tests where appropriate. Do not let the implementer silently edit or overwrite reviewer reports.
4. Rebuild and replay original failed tasks on target device/simulator. Capture new screenshot/video + logs tied to a build ID; old screenshots cannot count as post-fix verification.
5. Reassign original three roles to inspect new evidence in isolation (fresh sessions if possible), update finding status only with replay proof. Run `gamekit.py review evaluate --dir <new-run-folder>`.
6. At most 3 useful repair/review cycles. Stop and report remaining blockers rather than declare a synthetic 9/10. Do not push/merge without explicit instruction.

## Output contract

Baseline/final builds; raw triad reports for EACH cycle; consolidated deduplicated issues with owners; git diffs; test and task results; fresh post-fix captures; 5-axis scores per reviewer with proof; remaining P0/P1; gate result PASS/NOT APPROVED. A single-agent mock triad is PROVISIONAL, not an independent sign-off. No invented tool execution.

If any real runtime, independent reviewer context, screenshot or essential task evidence is absent, mark that check `NOT RUN / BLOCKED` and do not certify a 9/10 release.
