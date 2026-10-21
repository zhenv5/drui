# Purposeful game UI motion, stories and visual effects

Make a motion map from user intent: action → immediate state feedback → confirmation → return to stable resting state. Propose no more than one hero animation per screen. For onboarding/long scroll experiences, optionally use subtle parallax/continuous-shot transitions if they explain place or progress; avoid scroll storytelling in a timed answer view. Always design a reduced-motion alternative.

Implement original, reusable light trails, dot patterns and flowing gradients only when they serve navigation, scoring or energy/progress feedback. Suggested implementations: path-based SwiftUI Canvas glow, fixed lattice dots, time-varying gradients; or SpriteKit particles for play scenes. Keep interactive hit targets on top, math text dynamic, and track shadow/blur overdraw. Check 60fps on the baseline target, memory and battery, reduced-motion, color contrast and no flashing. `examples/OilUIEffectsGallery.swift` provides native iOS sample source; not a substitute for real hardware tests.

For every motion: write why it is useful, what action triggers it, duration/easing, disabled state, Reduce Motion fallback, worst-case cost and test steps. If art or 3D tooling is missing, do not claim generation success.
