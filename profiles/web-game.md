## Platform: Browser game

- Confirm mobile Safari/Chrome, desktop input and orientation targets. Use HTML Canvas/WebGL/DOM as appropriate.
- Test mouse, touch, keyboard/gamepad only if supported. Ensure responsive scaling, DPR and touch hit testing agree.
- Use browser automation to capture runtime screenshots for actual resolutions; test full game loop and reload state.

## UI review pipeline

Use `drui` and pre-existing `oil-ui` when available, then implement with this platform's native components. Inspect a real viewport/capture and the complete primary task, not just static design tokens. Mark visual QA NOT RUN without a real render.
