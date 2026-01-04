import SwiftUI

struct CardButtonStyle: ButtonStyle {
    var cornerRadius: CGFloat = CornerRadius.md

    func makeBody(configuration: Configuration) -> some View {
        configuration.label
            .frame(maxWidth: .infinity, alignment: .leading)
            .padding()
            .background(Color.appCardBackground)
            .cornerRadius(cornerRadius)
            .shadow(color: Color.black.opacity(0.1), radius: 2, x: 0, y: 1)
            .scaleEffect(configuration.isPressed ? 0.97 : 1.0)
            .opacity(configuration.isPressed ? 0.85 : 1.0)
            .animation(.easeInOut(duration: 0.15), value: configuration.isPressed)
    }
}

struct CardButtonStyle_Previews: PreviewProvider {
    static var previews: some View {
        VStack(spacing: 20) {
            Button {
                // action
            } label: {
                Label("Add File", systemImage: "plus")
            }
            .buttonStyle(CardButtonStyle())

            Button {
                // action
            } label: {
                Text("Continue")
            }
            .buttonStyle(CardButtonStyle(cornerRadius: 12))
        }
        .padding()
        .background(Color.appBackground)
        .previewLayout(.sizeThatFits)
        .environment(\.colorScheme, .light)

        VStack(spacing: 20) {
            Button {
                // action
            } label: {
                Label("Add File", systemImage: "plus")
            }
            .buttonStyle(CardButtonStyle())

            Button {
                // action
            } label: {
                Text("Continue")
            }
            .buttonStyle(CardButtonStyle(cornerRadius: 12))
        }
        .padding()
        .background(Color.appBackground)
        .previewLayout(.sizeThatFits)
        .environment(\.colorScheme, .dark)
    }
}
