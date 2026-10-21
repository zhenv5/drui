import SwiftUI

/// Original iOS 17+ motion ideas; not Oil UI Pro effects.
/// Review GPU/frame pacing and Reduce Motion on a physical device before using in production.
@available(iOS 17.0, *)
struct OilUIEffectsGallery: View {
    @Environment(\.accessibilityReduceMotion) private var reduceMotion

    var body: some View {
        ScrollView {
            VStack(spacing: 18) {
                Text("Original Game UI Effects")
                    .font(.title2.bold())
                    .frame(maxWidth: .infinity, alignment: .leading)
                section("Light trail (focus/selection)") { OilUILightTrail(reduceMotion: reduceMotion) }
                section("Dot pattern (quiet texture)") { OilUIDotPattern() }
                section("Flowing gradient (reward emphasis)") { OilUIFlowGradient(reduceMotion: reduceMotion) }
            }.padding(20)
        }
        .background(Color(red: 0.965, green: 0.97, blue: 0.985).ignoresSafeArea())
    }

    private func section<Content: View>(_ title: String, @ViewBuilder content: () -> Content) -> some View {
        VStack(alignment: .leading, spacing: 10) {
            Text(title).font(.headline)
            content().frame(height: 120)
                .frame(maxWidth: .infinity)
                .clipShape(RoundedRectangle(cornerRadius: 20))
        }
    }
}

@available(iOS 17.0, *)
private struct OilUILightTrail: View {
    let reduceMotion: Bool

    var body: some View {
        TimelineView(.animation(paused: reduceMotion)) { clock in
            let shift = reduceMotion ? 0.0 : sin(clock.date.timeIntervalSinceReferenceDate * 1.2) * 14
            Canvas { context, size in
                var path = Path()
                path.move(to: CGPoint(x: 22, y: size.height * 0.70))
                path.addQuadCurve(to: CGPoint(x: size.width - 22, y: size.height * 0.35 + shift),
                                  control: CGPoint(x: size.width * 0.48, y: size.height * 0.02 + shift))
                context.stroke(path, with: .color(.cyan.opacity(0.19)),
                               style: StrokeStyle(lineWidth: 22, lineCap: .round))
                context.stroke(path, with: .linearGradient(Gradient(colors: [.mint, .cyan, .indigo]),
                                                          startPoint: .zero,
                                                          endPoint: CGPoint(x: size.width, y: size.height)),
                               style: StrokeStyle(lineWidth: 5, lineCap: .round))
            }
        }
        .background(Color(red: 0.03, green: 0.15, blue: 0.25))
        .accessibilityLabel("Curved light trail, decorative")
    }
}

@available(iOS 17.0, *)
private struct OilUIDotPattern: View {
    var body: some View {
        Canvas { context, size in
            for x in stride(from: 14.0, through: size.width, by: 20.0) {
                for y in stride(from: 14.0, through: size.height, by: 20.0) {
                    let dot = Path(ellipseIn: CGRect(x: x, y: y, width: 3, height: 3))
                    context.fill(dot, with: .color(.teal.opacity(0.27)))
                }
            }
        }
        .background(Color(red: 0.92, green: 0.975, blue: 0.96))
        .accessibilityHidden(true)
    }
}

@available(iOS 17.0, *)
private struct OilUIFlowGradient: View {
    let reduceMotion: Bool

    var body: some View {
        TimelineView(.animation(paused: reduceMotion)) { clock in
            let turn = reduceMotion ? 0.0 : clock.date.timeIntervalSinceReferenceDate * 9.0
            ZStack {
                AngularGradient(colors: [.orange, .pink, .purple, .blue, .orange], center: .center)
                    .rotationEffect(.degrees(turn))
                LinearGradient(colors: [.white.opacity(0.20), .clear],
                               startPoint: .topLeading, endPoint: .bottomTrailing)
            }
        }
        .accessibilityLabel("Slowly changing colorful gradient, decorative")
    }
}

@available(iOS 17.0, *)
#Preview { OilUIEffectsGallery() }
