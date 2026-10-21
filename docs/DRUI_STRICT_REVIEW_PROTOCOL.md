# DRUI v1.4 — strict three-lens independent review protocol

## Independent by process, not by claimed title

- Tech Lead (TL) checks implementation quality/reliability, PM checks problem/value/flow, User lens checks first-use behavior on an actually running application. These are **review perspectives**, not evidence that an external human or licensed expert performed testing.
- Preferred: separate fresh agent sessions, no exposure to the other reviewers' notes or scores before first submission; independent read-only outputs. Store distinct `session_id` and `independence=isolated-session`.
- Fallback: one Agent may run three sequential passes **only if** marked `single-session`; this is PROVISIONAL, not an independent pass. Parallel subagents may still share training/assumptions; independence of judgments needs human spot checks.
- No reviewer is allowed to change source, tests, acceptance criteria or another review. Reviewer agents cannot sign off their own fixes.

## Evidence levels

1. E0: interpretation from requirements only — cannot score execution quality.
2. E1: static source/compile/test evidence — can support implementation claims, **not** actual UI/UX.
3. E2: real running app screenshots / recordings and replayable user tasks — required for visual/UX pass; include build ID and device.
4. E3: independent human user testing — strongest, distinct from simulated user lens; don't claim it happened unless real.

## Severity, arbitration and stopping

- P0: crash, core task impossible, data loss, serious child-safety violation.
- P1: recurring failure, broken or undiscoverable primary interaction, serious legibility/accessibility, major regression.
- P2: significant friction, inconsistent visual hierarchy or poor feedback; fix as capacity permits.
- P3: polish/low-impact edge.
- Never waive P0/P1 by averaging or voting. Require reproduction steps, expected/actual, and verification evidence.
- Role score = unweighted mean of exactly 5 rubric axes. Approval threshold per role mean >=9.0 and each axis >=8.0; must have no unresolved P0/P1, all three role reports complete, actual run evidence present, distinct contexts, and no BLOCKED/NOT RUN.
- `review evaluate` validates structured reports and existence of evidence file paths ONLY. It does NOT prove screenshots are real or independent sessions are genuine. Release owner must inspect evidence manually.
- After 3 useful cycles with blockers remaining, STOP, state remaining issues and targeted next tests. Avoid performative loops and self-awarded 9.5s.

## Cross-role disagreement resolution

Report matrix fields: issue_id, source_role, evidence, disagreement, reproduced_by, severity, adjudication, acceptance_check. Prefer reproductions and real task outcomes over subjective taste. PM scope desire must not override core reliability; TL simplification must not erase the user's ability to complete tasks; user confusion is a product bug unless reproducible evidence contradicts it.

## Strict reviewer roles

See `prompts/drui/reviewers/*.md`. Each role is separately invokable with `workflow prompt --stage review-tl|review-pm|review-user` and needs actual evidence.


## UI method provenance

Before a review assign primary UI source in descending availability: official `oil-ui-pro` > original `oil-ui-plus` > open `oil-ui` > DRUI fallback. Write chosen name and direct evidence the SKILL.md was actually read in the report. When the user explicitly requests a lower source, honor that override and explain it; never label the original Plus as official paid Pro.
