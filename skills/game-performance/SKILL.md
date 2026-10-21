---
name: game-performance
description: Profile and optimize FPS, startup, memory, asset loading and battery behavior across mobile or web games. Invoke for lag, crashes, stutter, animation problems or release performance.
---

# Game performance

1. Establish baseline in target hardware/runtime.
2. Measure frame pacing (not just average FPS), memory, first interactive time and texture costs.
3. Instrument before guessing; verify no unnecessary animation loops or repeated state recomputation.
4. Reduce overdraw / texture resampling, decode off main thread where possible and avoid unbounded assets.
5. Re-measure and log before/after; check low-end device where available.
6. Avoid sacrificing input responsiveness or accessibility for cosmetic effects.
