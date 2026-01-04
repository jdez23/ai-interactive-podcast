import SwiftUI

struct HomeTabView: View {
    @StateObject private var appState = AppState.shared
    
    var body: some View {
        if #available(iOS 16.0, *) {
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
        } else {
            NavigationView {
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
}

#Preview {
    HomeTabView()
}
