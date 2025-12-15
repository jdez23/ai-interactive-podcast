import SwiftUI
import Combine

@MainActor
class AppState: ObservableObject {
    static let shared = AppState()
    
    @Published var selectedTab: Tab = .home
    @Published var selectedPodcast: Podcast?
    @Published var generatedPodcasts: [Podcast] = []
    @Published var downloadedPodcasts: [Podcast] = []
    
    private init() {}
    
    func switchToGenerate() {
        selectedTab = .generate
    }
    
    func addGeneratedPodcast(_ podcast: Podcast) {
        generatedPodcasts.insert(podcast, at: 0)
    }
    
    func openPlayer(podcast: Podcast) {
        selectedPodcast = podcast
    }
}
