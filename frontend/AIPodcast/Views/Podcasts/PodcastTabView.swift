import SwiftUI

struct PodcastTabView: View {
    var body: some View {
        NavigationStack {
            PodcastListView()
                .navigationTitle("Podcasts")
        }
    }
}

#Preview {
    PodcastTabView()
}
