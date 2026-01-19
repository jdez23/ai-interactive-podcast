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
        ZStack {
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
                        
                        // Error Message
                        if let errorMessage = viewModel.errorMessage {
                            HStack {
                                Image(systemName: "exclamationmark.triangle.fill")
                                    .foregroundColor(.red)
                                Text(errorMessage)
                                    .font(.caption)
                                    .foregroundColor(.red)
                            }
                            .padding()
                            .background(Color.red.opacity(0.1))
                            .cornerRadius(8)
                            .padding(.horizontal)
                        }
                        
                        // Ask AI Section
                        AskAISection(
                            question: $viewModel.questionText,
                            isProcessing: viewModel.isProcessingQuestion,
                            onSubmitText: viewModel.submitTextQuestion
                        )
                        .padding(.horizontal)
                        .padding(.bottom, Spacing.lg)
                    }
                }
            }
            
            // Answer Overlay
            if viewModel.showAnswer, let answer = viewModel.currentAnswer {
                Color.black.opacity(0.4)
                    .ignoresSafeArea()
                    .onTapGesture {
                        viewModel.dismissAnswer()
                    }
                
                AnswerDisplayView(
                    question: viewModel.lastAskedQuestion,
                    answer: answer,
                    isPlayingAnswer: viewModel.isPlayingAnswer,
                    onDismiss: viewModel.dismissAnswer,
                    onResume: viewModel.resumePlayback
                )
                .padding(Spacing.md)
                .transition(AnyTransition.scale.combined(with: .opacity))
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
        // For now, just use a generic title
        // In the future, this could come from podcast metadata
        "AI Podcast Episode"
    }
    
    private var podcastSubtitle: String {
        let count = podcast.documentIds.count
        if count == 0 {
            return "AI Generated Podcast"
        } else if count == 1 {
            return "Generated from 1 document"
        } else {
            return "Generated from \(count) documents"
        }
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
        progressPercentage: 100,
        createdAt: Date()
    ))
}
