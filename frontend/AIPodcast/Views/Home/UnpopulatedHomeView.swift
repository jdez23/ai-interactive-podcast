import SwiftUI
import UniformTypeIdentifiers

struct UnpopulatedHomeView: View {
    @StateObject private var appState = AppState.shared
    @StateObject private var viewModel = GenerateViewModel.shared
    @State private var showFilePicker = false
    
    var body: some View {
        ZStack {
            Color.black.ignoresSafeArea()
            
            VStack(spacing: 0) {
                Spacer()
                AddFileEmptyState(onAddFile: {
                    showFilePicker = true
                })
                Spacer()
            }
        }
        .fileImporter(
            isPresented: $showFilePicker,
            allowedContentTypes: [.pdf],
            allowsMultipleSelection: true
        ) { result in
            // Handle file selection
            viewModel.handleFileSelection(result)
            // Switch to Generate tab after files are selected
            appState.switchToGenerate()
        }
    }
}

#Preview {
    UnpopulatedHomeView()
}
