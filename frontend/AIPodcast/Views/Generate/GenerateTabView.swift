import SwiftUI
import UniformTypeIdentifiers

struct GenerateTabView: View {
    @StateObject private var viewModel = GenerateViewModel()
    
    var body: some View {
        NavigationStack {
            ZStack {
                VStack(spacing: 0) {
                    // Add File Section
                    AddFileSection(
                        hasFiles: !viewModel.selectedFiles.isEmpty,
                        onAddFile: { viewModel.showFilePicker = true }
                    )
                    .padding()
                    
                    // Selected Files List
                    if !viewModel.selectedFiles.isEmpty {
                        FileListView(
                            files: viewModel.selectedFiles,
                            onDelete: viewModel.removeFile
                        )
                    } else {
                        Spacer()
                    }
                    
                    // Generate Button
                    if viewModel.canGenerate {
                        GenerateButton(
                            isGenerating: viewModel.isGenerating,
                            onGenerate: viewModel.generatePodcast
                        )
                        .padding()
                    }
                }
                
                // Loading Overlay
                if viewModel.isGenerating {
                    LoadingOverlay()
                }
            }
            .navigationTitle("Generate")
            .fileImporter(
                isPresented: $viewModel.showFilePicker,
                allowedContentTypes: [.pdf],
                allowsMultipleSelection: true
            ) { result in
                viewModel.handleFileSelection(result)
            }
            .alert("Error", isPresented: $viewModel.showError) {
                Button("OK") { viewModel.errorMessage = nil }
            } message: {
                if let error = viewModel.errorMessage {
                    Text(error)
                }
            }
        }
    }
}

#Preview {
    GenerateTabView()
}
