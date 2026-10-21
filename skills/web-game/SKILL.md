---
name: web-game
description: Implement and validate interactive web games, including Canvas/WebGL touch play, responsive browser UI and automated screenshots. Invoke for browser games or prototypes.
---

# Web game

- Separate deterministic game-state reducer from Canvas/WebGL/DOM rendering.
- Correctly handle devicePixelRatio and screen resize without moving hitboxes.
- Support touch gestures and prevent browser scrolling only over active play surfaces.
- Keep images, audio and sprites preloaded; apply efficient sprite batching where necessary.
- Write smoke tests for control loop, score/retry, pause/resume and edge viewports.
- Run a browser and capture actual screenshots at mobile and desktop resolutions.
