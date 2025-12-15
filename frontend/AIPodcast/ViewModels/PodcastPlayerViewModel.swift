import SwiftUI
import Combine
import AVFoundation

@MainActor
class PodcastPlayerViewModel: ObservableObject {
    let podcast: Podcast
    
    @Published var isPlaying = false
    @Published var currentTime: TimeInterval = 0
    @Published var duration: TimeInterval = 0
    @Published var questionText = ""
    @Published var isProcessingQuestion = false
    
    private var player: AVPlayer?
    private var timeObserver: Any?
    
    init(podcast: Podcast) {
        self.podcast = podcast
        setupPlayer()
    }
    
    private func setupPlayer() {
        guard let audioUrlString = podcast.audioUrl,
              let url = URL(string: audioUrlString) else { return }
        
        player = AVPlayer(url: url)
        duration = Double(podcast.duration ?? 0)
        
        // Add time observer
        let interval = CMTime(seconds: 0.5, preferredTimescale: CMTimeScale(NSEC_PER_SEC))
        timeObserver = player?.addPeriodicTimeObserver(forInterval: interval, queue: .main) { [weak self] time in
            guard let self = self else { return }
            MainActor.assumeIsolated {
                self.currentTime = time.seconds
            }
        }
    }
    
    func togglePlayPause() {
        if isPlaying {
            player?.pause()
        } else {
            player?.play()
        }
        isPlaying.toggle()
    }
    
    func rewind() {
        guard let player = player else { return }
        let newTime = max(0, currentTime - 10)
        player.seek(to: CMTime(seconds: newTime, preferredTimescale: 1))
    }
    
    func startVoiceQuestion() {
        // TODO: Implement voice recording
        // For now, just show an alert
        print("Voice question not yet implemented")
    }
    
    func submitTextQuestion() {
        guard !questionText.isEmpty else { return }
        
        isProcessingQuestion = true
        
        Task {
            do {
                let response = try await APIService.shared.askQuestion(
                    podcastId: podcast.id,
                    questionText: questionText
                )
                
                // Pause current podcast
                player?.pause()
                isPlaying = false
                
                // Play answer audio
                if let answerAudioUrl = response.answerAudioUrl,
                   let answerUrl = URL(string: answerAudioUrl) {
                    playAnswerAudio(url: answerUrl)
                }
                
                // Clear question
                questionText = ""
                isProcessingQuestion = false
                
            } catch {
                print("Error asking question: \(error)")
                isProcessingQuestion = false
            }
        }
    }
    
    private func playAnswerAudio(url: URL) {
        let answerPlayer = AVPlayer(url: url)
        answerPlayer.play()
        
        // TODO: Resume podcast after answer finishes
    }
    
    deinit {
        if let observer = timeObserver {
            player?.removeTimeObserver(observer)
        }
    }
}
