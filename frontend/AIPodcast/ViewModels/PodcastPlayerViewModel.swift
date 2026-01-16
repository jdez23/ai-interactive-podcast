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
    @Published var currentAnswer: QuestionResponse?
    @Published var showAnswer = false
    @Published var errorMessage: String?
    @Published var lastAskedQuestion = ""
    
    private var player: AVPlayer?
    private var timeObserver: Any?
    
    init(podcast: Podcast) {
        self.podcast = podcast
        setupPlayer()
    }
    
    private func setupPlayer() {
        guard let audioUrlString = podcast.audioUrl else {
            print("⚠️ No audio URL available for podcast")
            return
        }
        
        let fullUrlString: String
        if audioUrlString.hasPrefix("http://") || audioUrlString.hasPrefix("https://") {
            fullUrlString = audioUrlString
        } else {
            let cleanPath = audioUrlString.hasPrefix("/") ? String(audioUrlString.dropFirst()) : audioUrlString
            fullUrlString = "\(Constants.apiBaseURL)/\(cleanPath)"
        }
        
        guard let url = URL(string: fullUrlString) else {
            print("⚠️ Invalid audio URL: \(fullUrlString)")
            return
        }
        
        print("🎵 Setting up player with URL: \(fullUrlString)")
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
        errorMessage = nil
        
        let askedQuestion = questionText
        
        Task {
            do {
                print("📝 Asking question at timestamp: \(currentTime)s")
                
                let response = try await APIService.shared.askQuestion(
                    podcastId: podcast.id,
                    questionText: askedQuestion,
                    timestamp: currentTime
                )
                
                print("✅ Received answer: \(response.answerText.prefix(50))...")
                print("📚 Sources: \(response.sources.joined(separator: ", "))")
                print("📊 Context: \(response.contextUsed.documentChunks) chunks, \(response.contextUsed.dialogueExchanges) exchanges")
                
                // Pause current podcast
                player?.pause()
                isPlaying = false
                
                // Show answer
                lastAskedQuestion = askedQuestion
                currentAnswer = response
                showAnswer = true
                
                // Clear question input
                questionText = ""
                isProcessingQuestion = false
                
            } catch let error as APIError {
                print("❌ API Error asking question: \(error.localizedDescription)")
                errorMessage = error.localizedDescription
                isProcessingQuestion = false
            } catch {
                print("❌ Error asking question: \(error.localizedDescription)")
                errorMessage = "Failed to get answer. Please try again."
                isProcessingQuestion = false
            }
        }
    }
    
    func dismissAnswer() {
        showAnswer = false
        currentAnswer = nil
    }
    
    func resumePlayback() {
        dismissAnswer()
        player?.play()
        isPlaying = true
    }
    
    deinit {
        if let observer = timeObserver {
            player?.removeTimeObserver(observer)
        }
    }
}
