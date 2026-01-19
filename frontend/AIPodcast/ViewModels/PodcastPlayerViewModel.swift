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
    @Published var isPlayingAnswer = false
    
    private var player: AVPlayer?
    private var answerPlayer: AVPlayer?
    private var acknowledgmentPlayer: AVPlayer?
    private var transitionPlayer: AVPlayer?
    private var timeObserver: Any?
    private var savedTimestamp: TimeInterval = 0
    
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
    
    func submitTextQuestion() {
        guard !questionText.isEmpty else { return }
        
        isProcessingQuestion = true
        errorMessage = nil
        
        let askedQuestion = questionText
        
        Task {
            do {
                // Wait for current dialogue chunk to end (estimated 8 seconds per chunk)
                let secondsPerChunk: TimeInterval = 8.0
                let currentChunkIndex = Int(currentTime / secondsPerChunk)
                let nextChunkTime = TimeInterval(currentChunkIndex + 1) * secondsPerChunk
                let waitTime = max(0.1, nextChunkTime - currentTime)
                
                print("⏳ Waiting \(waitTime)s for current chunk to end...")
                try await Task.sleep(nanoseconds: UInt64(waitTime * 1_000_000_000))
                
                // Save timestamp at end of chunk
                savedTimestamp = nextChunkTime
                
                print("📝 Asking question at timestamp: \(savedTimestamp)s")
                
                // Fade out podcast smoothly
                await fadeOutPodcast()
                
                // Get acknowledgment audio with question
                print("🎤 Getting acknowledgment...")
                let acknowledgment = try await APIService.shared.getAcknowledgment(question: askedQuestion)
                await playAcknowledment(audioUrl: acknowledgment.audioUrl)
                
                // Get answer
                let response = try await APIService.shared.askQuestion(
                    podcastId: podcast.id,
                    questionText: askedQuestion,
                    timestamp: savedTimestamp
                )
                
                print("✅ Received answer: \(response.answerText.prefix(50))...")
                
                // Show answer
                lastAskedQuestion = askedQuestion
                currentAnswer = response
                showAnswer = true
                
                // Clear question input
                questionText = ""
                isProcessingQuestion = false
                
                // Play audio response if available
                if let audioUrl = response.audioUrl {
                    await playAnswerAudio(audioUrl: audioUrl)
                }
                
                // Play transition
                print("🔄 Getting transition...")
                let transition = try await APIService.shared.getReturnTransition()
                await playTransition(audioUrl: transition.audioUrl)
                
                // Resume podcast with fade in
                if let player = player {
                    await player.seek(to: CMTime(seconds: savedTimestamp, preferredTimescale: 1))
                }
                await fadeInPodcast()
                
                // Dismiss answer overlay
                showAnswer = false
                currentAnswer = nil
                
                print("✅ Completed Q&A flow")
                
            } catch let error as APIError {
                print("❌ API Error asking question: \(error.localizedDescription)")
                errorMessage = error.localizedDescription
                isProcessingQuestion = false
                // Resume podcast on error
                await fadeInPodcast()
            } catch {
                print("❌ Error asking question: \(error.localizedDescription)")
                errorMessage = "Failed to get answer. Please try again."
                isProcessingQuestion = false
                // Resume podcast on error
                await fadeInPodcast()
            }
        }
    }
    
    private func fadeOutPodcast() async {
        print("🔉 Fading out podcast...")
        guard let player = player else { return }
        
        let fadeSteps = 15
        let fadeDuration: TimeInterval = 1.0
        let stepDuration = fadeDuration / TimeInterval(fadeSteps)
        let initialVolume = player.volume
        let volumeStep = initialVolume / Float(fadeSteps)
        
        for _ in 0..<fadeSteps {
            player.volume = max(0, player.volume - volumeStep)
            try? await Task.sleep(nanoseconds: UInt64(stepDuration * 1_000_000_000))
        }
        
        player.pause()
        isPlaying = false
        player.volume = 1.0 // Reset for later
        print("✅ Podcast faded out")
    }
    
    private func fadeInPodcast() async {
        print("🔊 Fading in podcast...")
        guard let player = player else { return }
        
        player.volume = 0
        player.play()
        isPlaying = true
        
        let fadeSteps = 15
        let fadeDuration: TimeInterval = 1.0
        let stepDuration = fadeDuration / TimeInterval(fadeSteps)
        let volumeStep = 1.0 / Float(fadeSteps)
        
        for _ in 0..<fadeSteps {
            player.volume = min(1.0, player.volume + volumeStep)
            try? await Task.sleep(nanoseconds: UInt64(stepDuration * 1_000_000_000))
        }
        
        print("✅ Podcast faded in")
    }
    
    private func playAcknowledment(audioUrl: String) async {
        print("🎤 Playing acknowledgment...")
        
        let fullUrlString: String
        if audioUrl.hasPrefix("http://") || audioUrl.hasPrefix("https://") {
            fullUrlString = audioUrl
        } else {
            let cleanPath = audioUrl.hasPrefix("/") ? String(audioUrl.dropFirst()) : audioUrl
            fullUrlString = "\(Constants.apiBaseURL)/\(cleanPath)"
        }
        
        guard let url = URL(string: fullUrlString) else {
            print("⚠️ Invalid acknowledgment audio URL")
            return
        }
        
        let player = AVPlayer(url: url)
        self.acknowledgmentPlayer = player
        player.play()
        
        // Wait 3 seconds for acknowledgment
        try? await Task.sleep(nanoseconds: 3_000_000_000)
        print("✅ Acknowledgment finished")
    }
    
    private func playAnswerAudio(audioUrl: String) async {
        print("🎵 Playing answer audio...")
        
        let fullUrlString: String
        if audioUrl.hasPrefix("http://") || audioUrl.hasPrefix("https://") {
            fullUrlString = audioUrl
        } else {
            let cleanPath = audioUrl.hasPrefix("/") ? String(audioUrl.dropFirst()) : audioUrl
            fullUrlString = "\(Constants.apiBaseURL)/\(cleanPath)"
        }
        
        guard let url = URL(string: fullUrlString) else {
            print("⚠️ Invalid answer audio URL")
            return
        }
        
        let player = AVPlayer(url: url)
        self.answerPlayer = player
        self.isPlayingAnswer = true
        
        await withCheckedContinuation { [weak self] (continuation: CheckedContinuation<Void, Never>) in
            NotificationCenter.default.addObserver(
                forName: .AVPlayerItemDidPlayToEndTime,
                object: player.currentItem,
                queue: .main
            ) { _ in
                Task { @MainActor in
                    self?.isPlayingAnswer = false
                    print("✅ Answer audio finished")
                    continuation.resume()
                }
            }
            
            player.play()
        }
    }
    
    private func playTransition(audioUrl: String) async {
        print("🔄 Playing transition...")
        
        let fullUrlString: String
        if audioUrl.hasPrefix("http://") || audioUrl.hasPrefix("https://") {
            fullUrlString = audioUrl
        } else {
            let cleanPath = audioUrl.hasPrefix("/") ? String(audioUrl.dropFirst()) : audioUrl
            fullUrlString = "\(Constants.apiBaseURL)/\(cleanPath)"
        }
        
        guard let url = URL(string: fullUrlString) else {
            print("⚠️ Invalid transition audio URL")
            return
        }
        
        let player = AVPlayer(url: url)
        self.transitionPlayer = player
        player.play()
        
        // Wait 3 seconds for transition
        try? await Task.sleep(nanoseconds: 3_000_000_000)
        print("✅ Transition finished")
    }
    
    @MainActor
    func stopAnswerAudio() {
        answerPlayer?.pause()
        answerPlayer = nil
        acknowledgmentPlayer?.pause()
        acknowledgmentPlayer = nil
        transitionPlayer?.pause()
        transitionPlayer = nil
        isPlayingAnswer = false
    }
    
    func dismissAnswer() {
        stopAnswerAudio()
        showAnswer = false
        currentAnswer = nil
    }
    
    func resumePlayback() {
        stopAnswerAudio()
        dismissAnswer()
        if let player = player {
            player.seek(to: CMTime(seconds: savedTimestamp, preferredTimescale: 1))
            player.play()
            isPlaying = true
        }
    }
    
    deinit {
        if let observer = timeObserver {
            player?.removeTimeObserver(observer)
        }
        answerPlayer?.pause()
        answerPlayer = nil
        acknowledgmentPlayer?.pause()
        acknowledgmentPlayer = nil
        transitionPlayer?.pause()
        transitionPlayer = nil
        NotificationCenter.default.removeObserver(self)
    }
}
