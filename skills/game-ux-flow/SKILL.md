---
name: game-ux-flow
description: Review and improve game menus, onboarding, touch controls, state changes and accessibility. Invoke for usability, unclear actions, small hit targets or broken screen flow.
---

# Game UX flow

1. Reconstruct flows from an actual fresh install: first launch → start → understand controls → act → wrong/correct outcome → retry/continue → pause/resume.
2. For each view identify exactly one primary next action, easy exit, and clear game state.
3. Verify touch target sizes on phones (aim ~48–56 pt for major child controls when appropriate), gestures including cancellation, accessibility labels and no accidental double submissions.
4. Test iPhone/iPad target orientation, smallest supported viewport, safe area, dynamic type and reduced motion.
5. Eliminate confusing controls; support tutorial in-context without walls of text; preserve game rules.
6. Record findings with reproduction steps and verify against the actual runtime.

## Optional Oil UI companion

Route confusing UI to `drui` using mode `Flow fix` before cosmetic redesign. Execute an end-to-end task in the actual app, including error recovery and narrow-screen checks.
