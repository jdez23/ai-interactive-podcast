import SwiftUI

struct HomeTabView: View {
    @StateObject private var appState = AppState.shared
    
    var body: some View {
        NavigationStack {
            Group {
                if appState.generatedPodcasts.isEmpty && appState.downloadedPodcasts.isEmpty {
                    UnpopulatedHomeView()
                } else {
                    PopulatedHomeView()
                }
            }
            .navigationTitle("Home")
        }
    }
}

#Preview {
    HomeTabView()
}
