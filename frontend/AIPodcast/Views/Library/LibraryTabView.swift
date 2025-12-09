import SwiftUI

struct LibraryTabView: View {
    var body: some View {
        NavigationStack {
            VStack(spacing: 20) {
                Image(systemName: "books.vertical.fill")
                    .font(.system(size: 60))
                    .foregroundColor(.blue)
                
                Text("Your Library")
                    .font(.title)
                
                Text("Saved podcasts and documents will appear here")
                    .font(.subheadline)
                    .foregroundColor(.secondary)
                    .multilineTextAlignment(.center)
                    .padding()
            }
            .navigationTitle("Library")
        }
    }
}

#Preview {
    LibraryTabView()
}
