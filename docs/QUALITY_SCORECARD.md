# Evidence-based Game QA Rubric

Score each axis 0–5 with evidence, not intuition alone:

| Axis | 5 means | Required evidence |
|---|---|---|
| Player clarity | New player finds and understands primary action quickly | Fresh install walkthrough |
| Controls | Touch/gamepad/keyboard reliable, accurate and accessible | Recorded interactions at target size |
| Game feel | Immediate, meaningful feedback and smooth transitions | Real runtime capture and timings |
| Visual quality | Cohesive assets, legible UI, polished hierarchy | Actual screenshots vs approved references |
| Gameplay | Fair, varied, progressive and resilient | Level/logic tests and playthrough |
| Stability | No regressions, lifecycle failures or state races | Test and build logs |
| Performance | Acceptable device frame pacing/load | Profiling data |
| Accessibility | Text contrast, targets, reduced motion as appropriate | Explicit checks |

Release blockers: P0 crash/corrupted state, blocked core action, incorrect gameplay result, missing data preservation, child safety regression, false validation claims.

Evidence states: PASS (observed), FAIL (observed), BLOCKED (no environment/access), NOT RUN (not attempted). Blocked/Not Run are never counted as passes.

Report: findings → patch/diff → actual build/test commands → screenshots/artifact names → unresolved issues/risks.

## Oil UI independent review gate

For UI-heavy work, DRUI selects one UI method: installed official `oil-ui-pro` > original bundled `oil-ui-plus` > open `oil-ui` > DRUI fallback. DRUI always orchestrates QA. Maintain an additional **0–10 weighted UI scorecard** under `docs/OIL_UI_REVIEW_RUBRIC.md`. Report actual user task completion and capture evidence; target >=9 only if observed. Missing Oil UI is NOT AVAILABLE, not a failed package install, and not a successful review.
