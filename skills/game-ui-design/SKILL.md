---
name: game-ui-design
description: Design visually coherent game screens, HUDs, buttons and reward systems. Invoke when refining visual hierarchy, colors, typography, art/UI consistency or polish.
---

# Game UI design

Use when game screens look generic or inconsistent.

1. Identify the game's genre, audience, visual reference, and accessibility needs from its own materials. Do not import another game's brand.
2. Inspect **actual rendered screens** and inventory assets, navigation, title/CTA, playfield, menus and states. Distinguish a concept image from real runtime output.
3. Create a compact design system: color roles, type scale, spacing, panel elevation, interactive states, illustration language, asset sizes.
4. Refine one representative playable screen before rolling design to the rest. Prioritize focal point, legibility, and input clarity over ornaments.
5. Check smallest target device, large text, safe areas, and low-contrast/distracting backgrounds.
6. Produce actual code/assets changes plus screenshot evidence; no unimplemented mockup is a pass.

**Anti-patterns:** giant blurred backgrounds under small buttons; AI-generated math text baked into images; random icon styles; congratulating the player for invalid input; flattening interactive UI into a poster.

## Independent Oil UI quality gate

For UI reviews, invoke the owner's existing `oil-ui` if installed, then `drui`. Use `prompts/OIL_UI_ENHANCED_WORKFLOW.md` for mode selection, distinct design directions, screen recreation, anti-defaults, practical interactions and a scored review after rendering. This is original companion guidance, **not Oil UI Pro**. Don't claim 9/10 without runtime evidence.
