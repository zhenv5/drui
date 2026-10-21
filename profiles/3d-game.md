## Platform: 3D game (Unity, Unreal, Godot, custom)

- Preserve engine and asset pipeline unless explicitly changing them. Review animation rigs, camera, controls and collision boundaries.
- For 3D art, track source, licence, polygon budget, textures, LOD and lighting; separate previews from game assets.
- Require an actual engine build/frame capture to validate performance and image quality.

## UI review pipeline

Use `drui` and pre-existing `oil-ui` when available, then implement with this platform's native components. Inspect a real viewport/capture and the complete primary task, not just static design tokens. Mark visual QA NOT RUN without a real render.
