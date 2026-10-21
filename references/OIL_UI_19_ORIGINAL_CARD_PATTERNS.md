# 19 original card types for native / web games

These are **new, non-Pro** patterns for learning, prototyping and game production, not a copy of Oil UI Pro's paid card library. Each should be treated as a stateful interaction that may expand into a detail layer; use a single consistent token system and progressively disclose details. See `examples/OilUICardGallery.swift` for a SwiftUI gallery; the code is a reference, not a production drop-in without real asset and accessibility checks.

| # | Pattern | Primary role | Expanded detail / interaction |
|---|---|---|---|
| 01 | Hero Adventure | welcome/CTA | mission, start, accessibility |
| 02 | Level Token | selectable level | requirements, rewards, start |
| 03 | World Portal | themed world | level list and world history |
| 04 | Daily Streak | habit without pressure | last sessions, next optional goal |
| 05 | Treasure Chest | reward | reveal item, dismiss and resume |
| 06 | Progress Ribbon | long-term progress | per-world breakdown |
| 07 | Achievement | accomplishments | criteria and unlocked history |
| 08 | Choice Tile | branch selector | preview consequences before confirm |
| 09 | Math Challenge | immediate game task | hint, show legal input states |
| 10 | Inventory Item | supplies | quantity, equip/use/inspect |
| 11 | Soundscape | audio preview | independent music/effect toggles |
| 12 | Parent Insights | analytics | task-specific growth view |
| 13 | Hint Reveal | scaffold / guidance | progressive hint steps |
| 14 | Locked Quest | restriction clarity | unlock explanation and alternatives |
| 15 | Mission Brief | task context | success condition and tutorial |
| 16 | Gesture Coach | onboarding | step-by-step touch demonstration |
| 17 | Control Settings | adjustable controls | accessible options and defaults |
| 18 | Team Lobby | social optional games | status, invite, privacy labels |
| 19 | Spatial Inspector | layered summary | card-to-detail expansion with return |

## Implementation rules

- Every card has **one dominant action**, consistent 44pt minimum touch area (prefer bigger for children), and logical reading order.
- Expansion preserves location context and dismissibility, does not require precision swipes, and is keyboard/VoiceOver accessible when supported.
- Loading, unlocked/locked, empty, long-text, errors and reduce-motion must be tested.
- Avoid copying all 19 into one game; choose patterns that solve an actual screen need.
- Cards are view-model driven; titles, numbers and rewards must not be pre-rendered text within art images.

## Spatial expansion container contract

Trigger inside card -> stable identity -> expansion overlay/sheet -> task-specific details -> explicit close -> focus returns to originating card. Use `matchedGeometryEffect` where supported and simplify to a no-motion transition with Reduce Motion. Avoid nested interactive controls inside a single `Button`.
