import SwiftUI
import UniformTypeIdentifiers

struct GenerateTabView: View {
    @StateObject private var viewModel = GenerateViewModel.shared

    var body: some View {
        NavigationStack {
            ZStack {
                // Dark background
                Color.appBackground.ignoresSafeArea()
                VStack(spacing: 0) {
                    // Main content area
                    if viewModel.selectedFiles.isEmpty {
                        // Empty state - centered
                        Spacer()
                        AddFileEmptyState(onAddFile: { viewModel.showFilePicker = true })
                        Spacer()
                    } else {
                        // Files selected state
                        VStack(spacing: 0) {
                            // Add file box at top
                            AddFileBox(onAddFile: { viewModel.showFilePicker = true })
                                .padding()

                            // File list
                            FileListView(
                                files: viewModel.selectedFiles,
                                onDelete: viewModel.removeFile
                            )

                            Spacer()
                        }
                    }

                    // Generate Button - always visible
                    if !viewModel.selectedFiles.isEmpty {
                        GenerateButton(
                            isGenerating: viewModel.isGenerating,
                            onGenerate: viewModel.generatePodcast
                        )
                        .padding(.horizontal, 32)
                        .padding(.bottom, 20)
                    }
                }

                // Loading Overlay
                if viewModel.isGenerating {
                    LoadingOverlay()
                }
            }
            .navigationTitle("Generate")
            .navigationBarTitleDisplayMode(.large)
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
