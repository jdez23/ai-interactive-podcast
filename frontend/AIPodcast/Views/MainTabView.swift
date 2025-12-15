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
            
            LibraryTabView()
                .tabItem {
                    Label("Library", systemImage: "books.vertical.fill")
                }
                .tag(Tab.library)
        }
        .sheet(item: $appState.selectedPodcast) { podcast in
            PodcastPlayerView(podcast: podcast)
        }
    }
}

enum Tab {
    case home, generate, library
}

#Preview {
    MainTabView()
}
