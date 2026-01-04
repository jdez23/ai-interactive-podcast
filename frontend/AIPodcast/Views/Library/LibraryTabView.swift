import SwiftUI

struct LibraryTabView: View {
    var body: some View {
        if #available(iOS 16.0, *) {
            NavigationStack {
                VStack {
                    Text("Library Tab")
                        .font(.largeTitle)
                    Text("Coming soon...")
                        .foregroundColor(.secondary)
                }
                .navigationTitle("Library")
            }
        } else {
            NavigationView {
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
}

#Preview {
    LibraryTabView()
}
