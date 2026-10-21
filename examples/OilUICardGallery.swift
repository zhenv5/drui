import SwiftUI

/// Standalone ORIGINAL sample card-gallery for GameAgentKit, iOS 17+.
/// Not copied from or affiliated with any proprietary Oil UI Pro components.
/// Add to an iOS 17+ test target or SwiftUI sandbox to preview 19 interactive patterns.
@available(iOS 17.0, *)
struct OilUICardGallery: View {
    private struct Pattern: Identifiable {
        let id: Int
        let name: String
        let summary: String
        let symbol: String
        let tint: Color
    }

    private let patterns: [Pattern] = [
        .init(id: 1, name: "Hero Adventure", summary: "A clear entry point", symbol: "sparkles", tint: .orange),
        .init(id: 2, name: "Level Token", summary: "Choose the next challenge", symbol: "flag.checkered", tint: .mint),
        .init(id: 3, name: "World Portal", summary: "Explore the next world", symbol: "globe.europe.africa", tint: .teal),
        .init(id: 4, name: "Daily Streak", summary: "Gentle motivation", symbol: "flame", tint: .pink),
        .init(id: 5, name: "Treasure Chest", summary: "A meaningful reveal", symbol: "gift.fill", tint: .yellow),
        .init(id: 6, name: "Progress Ribbon", summary: "See the whole journey", symbol: "chart.bar.fill", tint: .green),
        .init(id: 7, name: "Achievement", summary: "Celebrate the milestone", symbol: "medal.fill", tint: .orange),
        .init(id: 8, name: "Choice Tile", summary: "Preview a branch", symbol: "arrow.triangle.branch", tint: .purple),
        .init(id: 9, name: "Math Challenge", summary: "Answer the next step", symbol: "plus.forwardslash.minus", tint: .indigo),
        .init(id: 10, name: "Inventory Item", summary: "Inspect your supplies", symbol: "shippingbox.fill", tint: .brown),
        .init(id: 11, name: "Soundscape", summary: "Listen before selecting", symbol: "waveform", tint: .cyan),
        .init(id: 12, name: "Parent Insights", summary: "Clarity without noise", symbol: "chart.xyaxis.line", tint: .blue),
        .init(id: 13, name: "Hint Reveal", summary: "Learn, don’t spoil", symbol: "lightbulb.fill", tint: .yellow),
        .init(id: 14, name: "Locked Quest", summary: "Explain what unlocks", symbol: "lock.fill", tint: .gray),
        .init(id: 15, name: "Mission Brief", summary: "Make the goal visible", symbol: "target", tint: .red),
        .init(id: 16, name: "Gesture Coach", summary: "Teach touch input", symbol: "hand.draw.fill", tint: .mint),
        .init(id: 17, name: "Control Settings", summary: "Accessible controls", symbol: "slider.horizontal.3", tint: .teal),
        .init(id: 18, name: "Team Lobby", summary: "Optional co-op flow", symbol: "person.2.fill", tint: .blue),
        .init(id: 19, name: "Spatial Inspector", summary: "Expand without losing place", symbol: "rectangle.expand.vertical", tint: .purple),
    ]

    @Namespace private var cardNamespace
    @State private var expanded: Int?
    @Environment(\.accessibilityReduceMotion) private var reduceMotion

    var body: some View {
        ZStack {
            Color(red: 0.965, green: 0.972, blue: 0.98).ignoresSafeArea()
            ScrollView {
                LazyVGrid(columns: [GridItem(.adaptive(minimum: 265), spacing: 14)], spacing: 14) {
                    ForEach(patterns) { pattern in
                        Button { open(pattern.id) } label: {
                            preview(for: pattern)
                                .frame(maxWidth: .infinity, alignment: .leading)
                                .frame(height: 154)
                                .padding(16)
                                .background(.white, in: RoundedRectangle(cornerRadius: 22))
                                .overlay(RoundedRectangle(cornerRadius: 22).strokeBorder(pattern.tint.opacity(0.25)))
                                .shadow(color: .black.opacity(0.07), radius: 10, y: 4)
                        }
                        .buttonStyle(.plain)
                        .matchedGeometryEffect(id: "card-\(pattern.id)", in: cardNamespace, isSource: expanded == nil)
                        .accessibilityLabel("\(pattern.name), \(pattern.summary), show details")
                    }
                }.padding(16)
            }
            .navigationTitle("19 Original Card Patterns")
            if let expanded, let pattern = patterns.first(where: { $0.id == expanded }) {
                Color.black.opacity(0.42).ignoresSafeArea()
                    .onTapGesture(perform: close)
                    .accessibilityLabel("Dismiss expanded card")
                detail(for: pattern)
                    .padding(22)
                    .frame(maxWidth: 470)
                    .frame(maxWidth: .infinity, maxHeight: .infinity)
                    .background(.white, in: RoundedRectangle(cornerRadius: 28))
                    .padding(24)
                    .matchedGeometryEffect(id: "card-\(pattern.id)", in: cardNamespace)
                    .zIndex(2)
            }
        }
    }

    private func open(_ id: Int) {
        withAnimation(reduceMotion ? nil : .spring(response: 0.36, dampingFraction: 0.84)) { expanded = id }
    }

    private func close() {
        withAnimation(reduceMotion ? nil : .easeOut(duration: 0.22)) { expanded = nil }
    }

    private func preview(for p: Pattern) -> some View {
        VStack(alignment: .leading, spacing: 12) {
            HStack {
                Image(systemName: p.symbol)
                    .font(.system(size: 28, weight: .bold))
                    .foregroundStyle(p.tint)
                    .frame(width: 44, height: 44)
                    .background(p.tint.opacity(0.13), in: RoundedRectangle(cornerRadius: 14))
                Spacer()
                Text(String(format: "%02d", p.id))
                    .font(.caption.monospacedDigit().weight(.bold))
                    .foregroundStyle(.secondary)
            }
            Text(p.name).font(.headline).foregroundStyle(.primary)
            Text(p.summary).font(.subheadline).foregroundStyle(.secondary).lineLimit(2)
            Spacer(minLength: 0)
            accent(for: p)
        }
    }

    @ViewBuilder private func accent(for p: Pattern) -> some View {
        switch p.id {
        case 2: ProgressView(value: 0.6).tint(p.tint)
        case 4: HStack(spacing: 6) {
            ForEach(0..<5, id: \.self) { i in Circle().fill(i < 3 ? p.tint : p.tint.opacity(0.15)).frame(width: 12, height: 12) }
        }
        case 6, 12: HStack(alignment: .bottom, spacing: 5) {
            ForEach([9, 15, 12, 21, 18], id: \.self) { x in
                RoundedRectangle(cornerRadius: 3).fill(p.tint.opacity(0.65)).frame(width: 12, height: CGFloat(x))
            }
        }
        case 9: Text("8 + 7 = ?").font(.title3.monospacedDigit().bold()).foregroundStyle(p.tint)
        case 14: Label("Finish level 4", systemImage: "lock").font(.caption).foregroundStyle(.secondary)
        case 19: Label("Tap to expand", systemImage: "arrow.up.left.and.arrow.down.right")
                .font(.caption.weight(.semibold)).foregroundStyle(p.tint)
        default: Capsule().fill(p.tint.opacity(0.18)).frame(height: 7)
        }
    }

    private func detail(for p: Pattern) -> some View {
        VStack(alignment: .leading, spacing: 18) {
            HStack {
                Image(systemName: p.symbol).font(.largeTitle).foregroundStyle(p.tint)
                Spacer()
                Button(action: close) { Image(systemName: "xmark.circle.fill").font(.title2) }
                    .accessibilityLabel("Close card details")
            }
            Text(p.name).font(.largeTitle.bold())
            Text(p.summary).font(.title3).foregroundStyle(.secondary)
            Divider()
            Text("Pattern \(p.id) / 19")
                .font(.footnote.weight(.semibold)).foregroundStyle(.secondary)
            Text(detailCopy(p.id)).font(.body)
            accent(for: p)
            Spacer(minLength: 0)
            Button("Close and return") { close() }
                .buttonStyle(.borderedProminent).tint(p.tint)
                .frame(maxWidth: .infinity)
        }
        .accessibilityElement(children: .contain)
    }

    private func detailCopy(_ id: Int) -> String {
        let descriptions = [
            "Entry point, mission and start action.", "Show rewards, prerequisites and a single Start CTA.",
            "Describe this world without embedding game text in the art.", "Show an optional reward, not a punitive streak.",
            "Reveal a reward, then return to the actual game.", "Expand into per-world progress while preserving totals.",
            "Show unlock criteria and the time it was earned.", "Preview consequences before confirming a choice.",
            "Drive math from live game state and show hint/error states.", "Show quantity, item meaning and available actions.",
            "Provide separate music/effects control and mute behavior.", "Expand learning trends into child-safe reporting.",
            "Reveal a small hint, then a second scaffold if needed.", "Explain the unlock condition and a reachable alternative.",
            "Clarify what success means before the task starts.", "Demonstrate tap or drag with a no-fail retry.",
            "Offer clear state, labels and reset defaults.", "Show participants, readiness and privacy controls.",
            "Expand spatially into focused detail and return context."
        ]
        return descriptions[min(max(id - 1, 0), descriptions.count - 1)]
    }
}

@available(iOS 17.0, *)
#Preview {
    NavigationStack { OilUICardGallery() }
}
