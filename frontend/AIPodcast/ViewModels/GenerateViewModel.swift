import SwiftUI
import Combine
import Foundation

struct SelectedFile: Identifiable {
    let id = UUID()
    let url: URL
    let name: String
    let size: Int64
    var uploadStatus: UploadStatus = .pending
    var documentId: String?

    var sizeString: String {
        ByteCountFormatter.string(fromByteCount: size, countStyle: .file)
    }
}

enum UploadStatus {
    case pending
    case uploading
    case success
    case error
}

extension SelectedFile {
    var documentStatus: DocumentCard.DocumentStatus {
        switch uploadStatus {
        case .pending, .success:
            return .ready
        case .uploading:
            return .uploading(progress: 1.0)
        case .error:
            return .failed
        }
    }
}

@MainActor
class GenerateViewModel: ObservableObject {
    static let shared = GenerateViewModel()
    
    @Published var selectedFiles: [SelectedFile] = []
    @Published var showFilePicker = false
    @Published var isGenerating = false
    @Published var generationProgress: Int = 0
    @Published var showError = false
    @Published var errorMessage: String?
    
    private var pollingTimer: Timer?
    private var currentPodcastId: String?
    
    private init() {}
    
    var canGenerate: Bool {
        !selectedFiles.isEmpty && selectedFiles.allSatisfy { $0.uploadStatus == .success }
    }
    
    func handleFileSelection(_ result: Result<[URL], Error>) {
        switch result {
        case .success(let urls):
            for url in urls {
                addFile(url: url)
            }
        case .failure(let error):
            errorMessage = error.localizedDescription
            showError = true
        }
    }
    
    private func addFile(url: URL) {
        guard url.startAccessingSecurityScopedResource() else { return }
        defer { url.stopAccessingSecurityScopedResource() }
        
        do {
            let attributes = try FileManager.default.attributesOfItem(atPath: url.path)
            let fileSize = attributes[.size] as? Int64 ?? 0
            
            // Check file size (50MB limit from Constants)
            if fileSize > Constants.maxFileSize {
                errorMessage = "File \(url.lastPathComponent) exceeds 50MB limit"
                showError = true
                return
            }
            
            let file = SelectedFile(
                url: url,
                name: url.lastPathComponent,
                size: fileSize
            )
            selectedFiles.append(file)
            
            // Auto-upload file
            uploadFile(file)
            
        } catch {
            errorMessage = "Could not read file: \(error.localizedDescription)"
            showError = true
        }
    }
    
    func removeFile(_ file: SelectedFile) {
        selectedFiles.removeAll { $0.id == file.id }
    }
    
    private func uploadFile(_ file: SelectedFile) {
        guard let index = selectedFiles.firstIndex(where: { $0.id == file.id }) else { return }
        
        selectedFiles[index].uploadStatus = .uploading
        
        Task {
            do {
                let document = try await APIService.shared.uploadDocument(fileURL: file.url)
                selectedFiles[index].uploadStatus = .success
                selectedFiles[index].documentId = document.id
            } catch {
                selectedFiles[index].uploadStatus = .error
                errorMessage = "Failed to upload \(file.name): \(error.localizedDescription)"
                showError = true
            }
        }
    }
    
    func generatePodcast() {
        guard canGenerate else { return }
        
        let documentIds = selectedFiles.compactMap { $0.documentId }
        guard !documentIds.isEmpty else {
            errorMessage = "No documents uploaded successfully"
            showError = true
            return
        }
        
        isGenerating = true
        generationProgress = 0
        
        Task {
            do {
                // Generate default topic from filenames
                let topic = selectedFiles.map { $0.name.replacingOccurrences(of: ".pdf", with: "") }.joined(separator: ", ")
                
                print("🎙️ Starting podcast generation...")
                
                // 1. Initiate generation
                let podcast = try await APIService.shared.generatePodcast(
                    documentIds: documentIds,
                    topic: topic,
                    durationMinutes: 3
                )
                
                await MainActor.run {
                    currentPodcastId = podcast.id
                    generationProgress = podcast.progressPercentage
                    print("🎙️ Podcast initiated: \(podcast.id), initial progress: \(generationProgress)%")
                }
                
                // Wait a moment for backend to start processing
                try await Task.sleep(nanoseconds: 500_000_000) // 0.5 seconds
                
                await MainActor.run {
                    // Start polling with a timer
                    startPolling()
                }
                
            } catch {
                await MainActor.run {
                    print("🎙️ Error: \(error.localizedDescription)")
                    isGenerating = false
                    generationProgress = 0
                    errorMessage = "Failed to generate podcast: \(error.localizedDescription)"
                    showError = true
                }
            }
        }
    }
    
    private func startPolling() {
        print("🎙️ Starting polling timer...")
        pollingTimer?.invalidate()
        
        pollingTimer = Timer.scheduledTimer(withTimeInterval: 1.0, repeats: true) { [weak self] _ in
            Task { @MainActor [weak self] in
                guard let self = self, let podcastId = self.currentPodcastId else { return }
                await self.checkPodcastStatus(podcastId: podcastId)
            }
        }
        
        // Fire immediately
        pollingTimer?.fire()
    }
    
    private func checkPodcastStatus(podcastId: String) async {
        do {
            print("🎙️ Checking status for \(podcastId)...")
            let status = try await APIService.shared.getPodcastStatus(podcastId: podcastId)
            
            generationProgress = status.progressPercentage
            print("🎙️ Progress: \(generationProgress)%, Status: \(status.status)")
            
            if status.status == .ready {
                print("🎙️ Podcast complete!")
                pollingTimer?.invalidate()
                generationProgress = 100
                AppState.shared.addGeneratedPodcast(status)
                AppState.shared.openPlayer(podcast: status)
                selectedFiles.removeAll()
                isGenerating = false
                currentPodcastId = nil
            } else if status.status == .failed {
                print("🎙️ Podcast generation failed")
                pollingTimer?.invalidate()
                isGenerating = false
                generationProgress = 0
                errorMessage = "Podcast generation failed"
                showError = true
                currentPodcastId = nil
            }
        } catch {
            print("🎙️ Error checking status: \(error.localizedDescription)")
            pollingTimer?.invalidate()
            isGenerating = false
            generationProgress = 0
            errorMessage = "Failed to check podcast status: \(error.localizedDescription)"
            showError = true
            currentPodcastId = nil
        }
    }
}
