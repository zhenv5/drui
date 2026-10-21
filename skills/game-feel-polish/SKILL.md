---
name: game-feel-polish
description: Improve input response, feedback animations, haptics, audio and progression feel. Invoke when game mechanics work but feel weak, delayed or unpleasant.
---

# Game feel polish

Measure and improve the response to player actions:

- Touch down: immediate visual pressed state with no artificial latency.
- Commit: clear positive/negative feedback, never falsely acknowledge an invalid move.
- Transition: hold successful result long enough to perceive, then move to next question/state.
- Reward: a brief layered animation, restrained haptic and sound that scale with achievement.
- Error: short and kind corrective feedback; allow safe reattempt; no long punishment.
- Pause: freeze gameplay transitions and pending timers; resume without duplicating events.
- Accessibility: reduced-motion route and adjustable audio; no flashing as sole signal.

Use instrumented runtime timings where possible; no fixed 'feels good' rating without testing.
