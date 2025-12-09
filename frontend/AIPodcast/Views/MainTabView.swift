import SwiftUI

struct MainTabView: View {
    var body: some View {
        TabView {
            DocumentTabView()
                .tabItem {
                    Label("Documents", systemImage: "doc.text.fill")
                }
            
            PodcastTabView()
                .tabItem {
                    Label("Podcasts", systemImage: "waveform")
                }
            
            LibraryTabView()
                .tabItem {
                    Label("Library", systemImage: "books.vertical.fill")
                }
        }
    }
}

#Preview {
    MainTabView()
}
