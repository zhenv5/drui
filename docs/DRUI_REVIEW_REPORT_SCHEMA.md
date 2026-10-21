# Strict triad JSON report contract

Run `python3 ~/GameAgentKit/gamekit.py review prepare --project /path/to/game --output /path/to/new-review-folder` to make one report template per reviewer and separate read-only prompt files. Fill the templates; the generated blank files are NOT evidence.

Fields in every `<role>.json`:

- `reviewer`: `tech-lead` / `product-manager` / `end-user`
- `session_id`: unique non-empty ID identifying a reviewer context (user-provided, not verified automatically)
- `independence`: `isolated-session` (fresh context) or `single-session` (provisional only)
- `scope`: tested build, platform, screen/task scope
- `source_changes`: `false` (must never edit implementation in review stages)
- `screens_examined`: nonempty array of concrete screen/state names
- `tasks_tested`: nonempty array containing task, steps, and outcome (e.g. strings, more detail welcome)
- `observations`: >=3 concrete grounded observations
- `evidence_files`: nonempty list of existing screenshot, recording, or log file paths relative to review folder or absolute
- `scores`: 5 exact axes as below, numeric 0–10, **no nulls for completed review**
- `findings`: array of `{id, severity, screen, evidence, repro_steps, expected, actual, recommendation, acceptance_test, status}`. Severity P0/P1/P2/P3. Status `open` / `fixed-unverified` / `verified`; unresolved P0/P1 fails release gate.
- `limitations`: array. Any entries starting BLOCKED, NOT RUN, UNVERIFIED block signoff.

Rubric axes:

- TL: `architecture`, `correctness`, `performance`, `maintainability`, `integration`.
- PM: `user_value`, `onboarding`, `flow`, `scope`, `retention`.
- User: `clarity`, `touch`, `feedback`, `confidence`, `enjoyment`.

Use an evidence filename relative to the folder, e.g. `evidence/ios-home-20261020.png`. A filename existing on disk does not guarantee it is a real device capture; make that distinction in human-facing conclusions. Do not use synthetic marketing or AI mockup pictures as UI runtime evidence. Formally approve only after replaying the critical tasks and a human checking the files.
