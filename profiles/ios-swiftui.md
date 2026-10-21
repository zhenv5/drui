## Platform: Native iOS / SwiftUI / SpriteKit

- Prioritize iPhone one-hand touch ergonomics, readable HUD, safe areas and smaller screen layouts; verify iPad separately if supported.
- Use SwiftUI for app structure and SpriteKit for gameplay effects/trails/sprites when suitable, preserving deterministic game logic.
- Build with Xcode on a Mac, run UI tests or scripted simctl flows and store actual screenshots tagged with simulator device name.
- Never count `swiftc -parse` as a successful Xcode compilation. Handle reduced motion and game lifecycle correctly.

## UI review pipeline

Use `drui` and pre-existing `oil-ui` when available, then implement with this platform's native components. Inspect a real viewport/capture and the complete primary task, not just static design tokens. Mark visual QA NOT RUN without a real render.
