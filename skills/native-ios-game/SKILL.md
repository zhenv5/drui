---
name: native-ios-game
description: Build and polish actual native iOS games using SwiftUI and SpriteKit. Invoke for iPhone/iPad UI, touch interaction, animations, Swift game state and Xcode verification.
---

# Native iOS game

Use SwiftUI for navigation, settings, overlays and data dashboards. Use SpriteKit or lower-level rendering where continuous interactive canvas, particles, trails or animated sprites benefit. Keep game logic testable and separated from rendering.

- Check minimum deployment version and existing architecture before changing files.
- Safe areas, 60 FPS target when feasible, no layout that hides input under home indicator.
- Clear cancellation/gesture ownership and single-action guards; stop tasks/timers when the state changes.
- Asset catalogs must contain real transparent/opaque images of supported sizes; never bake dynamic text/math into artwork.
- Run `xcodebuild` for actual compile, then `xcrun simctl`/UI testing for screenshots; if Mac unavailable, mark blocked.
- Confirm voiceover labels, reduced motion, and parent-only settings safety where applicable.
