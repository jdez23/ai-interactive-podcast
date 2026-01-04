import SwiftUI
import AVFoundation

struct PodcastPlayerView: View {
    let podcast: Podcast
    @StateObject private var viewModel: PodcastPlayerViewModel
    @Environment(\.dismiss) private var dismiss
    
    init(podcast: Podcast) {
        self.podcast = podcast
        _viewModel = StateObject(wrappedValue: PodcastPlayerViewModel(podcast: podcast))
    }
    
    private var content: some View {
        VStack(spacing: 0) {
            // Custom Nav Bar
            CustomNavBar(
                podcast: podcast,
                onDismiss: { dismiss() },
                onRewind: viewModel.rewind
            )
            
            ScrollView {
                VStack(spacing: 25) {
                    // Thumbnail
                    RoundedRectangle(cornerRadius: 20)
                        .fill(Color.gray.opacity(0.3))
                        .frame(width: 250, height: 250)
                        .overlay(
                            Image(systemName: "waveform")
                                .font(.system(size: 60))
                                .foregroundColor(.white)
                        )
                        .padding(.top, 30)
                    
                    // Progress Bar
                    ProgressBarView(
                        currentTime: viewModel.currentTime,
                        duration: viewModel.duration
                    )
                    .padding(.horizontal)
                    
                    // Title and Info
                    VStack(spacing: 8) {
                        Text(podcastTitle)
                            .font(.title2)
                            .fontWeight(.bold)
                            .multilineTextAlignment(.center)
                        
                        Text(podcastSubtitle)
                            .font(.subheadline)
                            .foregroundColor(.secondary)
                        
                        Text(durationText)
                            .font(.caption)
                            .foregroundColor(.secondary)
                    }
                    .padding(.horizontal)
                    
                    // Playback Controls
                    PlaybackControlsView(
                        isPlaying: viewModel.isPlaying,
                        onPlayPause: viewModel.togglePlayPause
                    )
                    .padding(.vertical)
                    
                    // Ask AI Section
                    AskAISection(
                        question: $viewModel.questionText,
                        isProcessing: viewModel.isProcessingQuestion,
                        onTapToAsk: viewModel.startVoiceQuestion,
                        onSubmitText: viewModel.submitTextQuestion
                    )
                    .padding(.horizontal)
                }
            }
        }
    }
    
    var body: some View {
        if #available(iOS 16.0, *) {
            NavigationStack {
                content
                    .navigationBarHidden(true)
            }
        } else {
            NavigationView {
                content
                    .navigationBarHidden(true)
            }
        }
    }
    
    private var podcastTitle: String {
        // Extract from podcast metadata or use default
        "Podcast Episode"
    }
    
    private var podcastSubtitle: String {
        "Generated from \(podcast.documentIds.count) document(s)"
    }
    
    private var durationText: String {
        if let duration = podcast.duration {
            let minutes = duration / 60
            let seconds = duration % 60
            return String(format: "%d:%02d", minutes, seconds)
        }
        return "--:--"
    }
}

#Preview {
    PodcastPlayerView(podcast: Podcast(
        id: "test",
        documentIds: ["doc1"],
        audioUrl: "http://localhost:8000/test.mp3",
        duration: 180,
        status: .ready,
        createdAt: Date()
    ))
}
