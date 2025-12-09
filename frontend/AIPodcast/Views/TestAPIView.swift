import SwiftUI

struct TestAPIView: View {
    @State private var statusMessage: String = "Ready to test"
    @State private var isLoading: Bool = false
    
    var body: some View {
        VStack(spacing: 20) {
            Text("API Service Test")
                .font(.title)
            
            Text(statusMessage)
                .foregroundColor(statusMessage.contains("✅") ? .green : .primary)
                .multilineTextAlignment(.center)
                .padding()
            
            if isLoading {
                ProgressView()
            }
            
            Button("Test Health Check") {
                testHealthCheck()
            }
            .disabled(isLoading)
            
            Button("Test Generate Podcast") {
                testGeneratePodcast()
            }
            .disabled(isLoading)
        }
        .padding()
    }
    
    func testHealthCheck() {
        isLoading = true
        statusMessage = "Testing health check..."
        
        Task {
            do {
                let response = try await APIService.shared.healthCheck()
                await MainActor.run {
                    statusMessage = "✅ Health check passed!\n\(response)"
                    isLoading = false
                }
            } catch {
                await MainActor.run {
                    statusMessage = "❌ Error: \(error.localizedDescription)"
                    isLoading = false
                }
            }
        }
    }
    
    func testGeneratePodcast() {
        isLoading = true
        statusMessage = "Testing podcast generation...\n(This requires uploaded documents)"
        
        Task {
            do {
                // Test with mock document IDs - replace with real ones if you have them
                let podcast = try await APIService.shared.generatePodcast(
                    documentIds: ["doc_test123"],
                    topic: "Test Podcast",
                    durationMinutes: 3
                )
                await MainActor.run {
                    statusMessage = "✅ Podcast generated!\nID: \(podcast.id)"
                    isLoading = false
                }
            } catch {
                await MainActor.run {
                    statusMessage = "❌ Error: \(error.localizedDescription)\n(This is expected without real document IDs)"
                    isLoading = false
                }
            }
        }
    }
}
