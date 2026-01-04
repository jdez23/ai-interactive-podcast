import SwiftUI

struct PodcastTabView: View {
    var body: some View {
        if #available(iOS 16.0, *) {
            NavigationStack {
                PodcastListView()
                    .navigationTitle("Podcasts")
            }
        } else {
            NavigationView {
                PodcastListView()
                    .navigationTitle("Podcasts")
            }
        }
    }
}

#Preview {
    PodcastTabView()
}
