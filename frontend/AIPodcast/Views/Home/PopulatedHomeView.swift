import SwiftUI

struct PopulatedHomeView: View {
    @StateObject private var appState = AppState.shared

    var body: some View {
        ScrollView {
            VStack(alignment: .leading, spacing: 25) {
                // Recently Generated Section
                if !appState.generatedPodcasts.isEmpty {
                    VStack(alignment: .leading, spacing: 12) {
                        Text("Recently Generated")
                            .font(.title2)
                            .fontWeight(.bold)
                            .padding(.horizontal)

                        ScrollView(.horizontal, showsIndicators: false) {
                            HStack(spacing: 15) {
                                ForEach(appState.generatedPodcasts) { podcast in
                                    PodcastCardView(podcast: podcast)
                                        .onTapGesture {
                                            appState.openPlayer(podcast: podcast)
                                        }
                                }
                            }
                            .padding(.horizontal)
                        }
                    }
                }

                // Downloaded Section
                if !appState.downloadedPodcasts.isEmpty {
                    VStack(alignment: .leading, spacing: 12) {
                        Text("Downloaded")
                            .font(.title2)
                            .fontWeight(.bold)
                            .padding(.horizontal)

                        ScrollView(.horizontal, showsIndicators: false) {
                            HStack(spacing: 15) {
                                ForEach(appState.downloadedPodcasts) { podcast in
                                    PodcastCardView(podcast: podcast)
                                        .onTapGesture {
                                            appState.openPlayer(podcast: podcast)
                                        }
                                }
                            }
                            .padding(.horizontal)
                        }
                    }
                }
            }
            .padding(.vertical)
        }
        .background(Color.black.ignoresSafeArea())
    }
}

#Preview {
    PopulatedHomeView()
}
