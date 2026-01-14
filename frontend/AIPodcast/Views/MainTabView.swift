import SwiftUI

struct MainTabView: View {
    @StateObject private var appState = AppState.shared

    var body: some View {
        TabView(selection: $appState.selectedTab) {
            HomeTabView()
                .tabItem {
                    Label("Home", systemImage: "house.fill")
                }
                .tag(Tab.home)

            GenerateTabView()
                .tabItem {
                    Label("Generate", systemImage: "sparkles")
                }
                .tag(Tab.generate)
        }
        .sheet(item: $appState.selectedPodcast) { podcast in
            PodcastPlayerView(podcast: podcast)
        }
    }
}

enum Tab {
    case home, generate
}

#Preview {
    MainTabView()
}
