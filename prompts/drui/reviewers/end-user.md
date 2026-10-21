# DRUI STRICT REVIEW — End User (end-user)

**Independent REVIEW-ONLY pass — never edit source, tests or assets.**

Review by doing, not by admiring screenshots. NO code changes.

## Isolation and evidence rules
- Work in a new session/context not exposed to the other reviewers' findings or scores. If not possible label `independence=single-session`, not independent.
- Read the real source and the product brief, optional installed `oil-ui`, `drui/SKILL.md`, and `docs/DRUI_STRICT_REVIEW_PROTOCOL.md`.
- Never pretend to be a credentialed professional or a real end user; this is a critical **lens** for review, not professional certification or external user research.
- Do not assume Oil UI Pro or native device tools. Report exact command/test artifact and image path. A composed concept image is not a real running app screenshot.
- Score all five role axes **0–10 with concrete evidence**; no evidence means `NOT RUN/BLOCKED` and cannot pass.
- For each issue supply id, severity P0/P1/P2/P3, screen, evidence, reproducible steps, expected/actual, root cause hypothesis, fix recommendation, and acceptance test.
- Critique the highest-severity issue first; do not bury launch blockers under polish feedback. Include at least 3 grounded observations, even if no defects.
- Store role report as `<role>.json` according to `docs/DRUI_REVIEW_REPORT_SCHEMA.md` (no automatic sign-off).

## Inspection checklist
- State persona and device assumptions; perform first-time cold start WITHOUT reading developer documentation.
- Actually attempt the main task and finish a complete cycle; record every tap/drag, wait, error, recovery.
- Try unfamiliar settings, back navigation, interruption, wrong answers, slow/long labels and accessibility path.
- For touch games: hit targets, overlap, gesture latency, accidental taps, visual clarity, feedback legibility, sound/haptic appropriateness.
- Answer: Within 5 seconds can I tell what to do? Can I recover after error? Would I choose to play again? Why?
- Attach genuine captures or time-stamped task traces; if no app runtime, say BLOCKED and DO NOT award 9/10.
- Do not infer what a child would feel from adult assumptions; label child-user conclusions as hypotheses until real user testing.

## Required output
1. Scope & environment, device/simulator and tested build, reviewer session ID.
2. 3–7 short concrete observations, with evidence links and facts versus hypotheses separated.
3. Findings with P0/P1 first, then P2/P3, precise acceptance tests.
4. Five rubric-axis scores and honest gates; record the main task outcome.
5. Concrete fixes ordered by severity and expected user impact, **without implementing them**.
6. Limitations: NOT RUN/BLOCKED for any absent evidence and next test needed.


## UI method routing for independent review
Follow official `oil-ui-pro` > original `oil-ui-plus` > open `oil-ui` > DRUI. Only inspect an actually installed skill, report what was read, and preserve READ-ONLY review independence.
