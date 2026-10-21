---
name: game-qa-review
description: Run independent multi-pass quality reviews of playable games with evidence. Invoke for review → fix → retest requests, game polish audits or pre-release signoff.
---

# Independent game QA — 3 passes

Use project-specific `.game-agent-kit/PROFILE.md` if it exists. Otherwise infer platform and ask only for critical unknowns.

## Pass 1: Player
On real runtime, inspect first-launch, clarity, basic controls, invalid actions, hints, pause, retries and progression. Fix the highest-impact defects.

## Pass 2: Art / UX
Review actual screenshots, text readability, touch areas, layout scaling, consistency of character and environment resources. Compare to supplied references. Fix P0/P1 and document asset gaps.

## Pass 3: Technical
Exercise game state transitions, tests, lifecycle, persistence, reduced-motion, input latency and performance. Retest previously fixed issues.

**Required evidence:** file/diff listing, exact test/build commands and outcomes, device/simulator screenshots with device name (if available), P0/P1 closure, and unresolved limitations.

**Hard gates:** never label syntax checks as Xcode/Unity builds; never label a conceptual composite as simulator screenshot; never claim unrun tests passed; don't push/merge without request.

## Oil UI visual independence

For any UI-heavy review, call/read external `oil-ui` when installed, then `drui`. Score per `docs/OIL_UI_REVIEW_RUBRIC.md` and re-run real user tasks after repairs. Use three independent roles and leave no invented visual scores or screenshots. Missing Oil UI is marked NOT AVAILABLE rather than a generic PASS.
