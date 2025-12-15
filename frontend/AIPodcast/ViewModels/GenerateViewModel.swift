import SwiftUI
import Combine

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

@MainActor
class GenerateViewModel: ObservableObject {
    @Published var selectedFiles: [SelectedFile] = []
    @Published var showFilePicker = false
    @Published var isGenerating = false
    @Published var showError = false
    @Published var errorMessage: String?
    
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
            
            // Check file size (10MB limit from Constants)
            if fileSize > Constants.maxFileSize {
                errorMessage = "File \(url.lastPathComponent) exceeds 10MB limit"
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
        
        Task {
            do {
                // Generate default topic from filenames
                let topic = selectedFiles.map { $0.name.replacingOccurrences(of: ".pdf", with: "") }.joined(separator: ", ")
                
                let podcast = try await APIService.shared.generatePodcast(
                    documentIds: documentIds,
                    topic: topic,
                    durationMinutes: 3
                )
                
                // Add to app state
                AppState.shared.addGeneratedPodcast(podcast)
                
                // Open player
                AppState.shared.openPlayer(podcast: podcast)
                
                // Reset state
                selectedFiles.removeAll()
                isGenerating = false
                
            } catch {
                isGenerating = false
                errorMessage = "Failed to generate podcast: \(error.localizedDescription)"
                showError = true
            }
        }
    }
}
