import SwiftUI

struct LibraryTabView: View {
    var body: some View {
        NavigationStack {
            VStack {
                Text("Library Tab")
                    .font(.largeTitle)
                Text("Coming soon...")
                    .foregroundColor(.secondary)
            }
            .navigationTitle("Library")
        }
    }
}

#Preview {
    LibraryTabView()
}
