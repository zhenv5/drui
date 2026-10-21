# Independent UI review rubric (original, evidence driven)

**Target 9/10; passing is not automatic.** Each axis scores 0.0–10.0; weighted average is reported to one decimal place. A score above 8 with no runtime evidence should be labelled **PROVISIONAL**, never PASS.

| Axis | Weight | What a 9–10 requires |
|---|---:|---|
| Product / visual direction | 15% | Cohesive brand, distinctive, not generic AI template |
| Hierarchy / readability | 15% | Key task immediately evident, correct type/contrast |
| UX / task completion | 20% | Main task completed by interacting with the actual app |
| Input / state coverage | 15% | Pressed, wrong, selected, loading, modal, disabled, retry etc verified where applicable |
| Responsive / access | 10% | Target devices, safe areas, Dynamic Type / keyboard and Reduce Motion considered |
| Scene / assets / motion | 15% | Consistent visual material, no blurry cutouts, purposeful animations |
| Code / performance stability | 10% | Tests, no new state races, reasonable performance for target hardware |

**Evidence:** source revisions + actual running screenshot/capture + test command + device/viewport + user-task steps. A concept render is NOT a running screenshot. Independent review means a fresh evaluation pass and new issue log, not rewording the implementation summary.

## Automatic rejection / rating caps

- No true rendering: score is *unverified*, cannot mark UI pass at any number.
- P0 crash, hidden primary action, math correctness regression, unfinishable task: FAIL, no 9/10 claim.
- P1 severe tap/drag errors, clipped content, broken transition: FAIL until fixed and rerendered.
- Design directions differ only in palette: reject overlap and redesign.
- Static screenshot behind invisible hitboxes: reject UI engineering gate.
- In-game scene over-decorated so task or targets unclear: reject simplicity gate.

## Three review cycles

1. **Visual art director:** composition, hierarchy, material cohesion, visual identity, simplify AI defaults.
2. **New user/UX:** cold task completion, UI states, error recovery, touch ergonomics, mobile/tablet behavior.
3. **Tech/perf/accessibility:** source, state regression, performance, dynamic type, reduced motion.

After each cycle: issue severity + evidence → implement fix → run tests → recapture → score again. Stop at <=3 cycles or when no material improvement can be evidenced. Output `NOT RUN`/`BLOCKED` where appropriate, and state next highest-impact blockers.

### Scorecard template

```text
UI goal / task: ...
Selected mode/direction: ...
Baseline screenshot: ... (device or NOT RUN)
Cycle # (role): ...
Findings: P0, P1, P2 with evidence
Fixes + files: ...
Task test steps/results: ...
After screenshot: ... (device or NOT RUN)
Scores: direction __/10, hierarchy __/10, task __/10,
        states __/10, responsive __/10, art/motion __/10, code __/10
Weighted overall: __/10 [VERIFIED or PROVISIONAL]
Open issues / blocked tests: ...
```
