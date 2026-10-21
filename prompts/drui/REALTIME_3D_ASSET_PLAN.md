# Mini-game 3D scene and generated-asset protocol

Before generating assets decide if 3D is actually necessary. If the game is 2.5D and native iOS, prefer baked scene background + independent alpha sprites + SwiftUI/SpriteKit dynamic overlay, not a whole 3D world. For genuine 3D, document coordinate system, camera projection, render style, target device GPU budget, lighting pipeline, scale/texture units, LOD and animation rig requirements.

### Single-asset brief

One object/character or background per generation job. Lock approved reference identity, silhouette, materials, eye color, proportions, camera and lighting, and requested poses. Reject UI collage, text baked into PNG, background matte, blurry upscale, inconsistent character identity, non-commercial rights or files too large for the target. Keep original generation settings and source/license notes.

### Real task validation

Render a character in the actual game at display size and inspect alpha, perspective, shadows, frame pacing and contrast against playfield. Test motion states idle/hint/error/success and transitions. For 3D check collision/interactivity, shader cost and fallback on target mobile GPU. Document which work was done in model, image generator, Blender/Loopcut/ComfyUI and which steps are NOT RUN. MCP or Skill availability is not proof of real asset generation.
