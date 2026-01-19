import SwiftUI

struct FileListView: View {
    let files: [SelectedFile]
    let onDelete: (SelectedFile) -> Void
    
    var body: some View {
        VStack(alignment: .leading, spacing: 16) {
            Text("Chosen Files (\(files.count))")
                .font(.appBody)
                .foregroundColor(.appPrimary)
                .padding(.horizontal, Spacing.md)
            
            // File list
            VStack(spacing: 8) {
                ForEach(files) { file in
                    DocumentCard(
                        filename: file.name,
                        status: file.documentStatus,
                        fileSize: file.sizeString,
                        onDelete: { onDelete(file) }
                    )
                }
            }
            .padding(.horizontal, Spacing.md)
        }
    }
}

#Preview {
    ZStack {
        Color.white.ignoresSafeArea()
        
        FileListView(
            files: [
                SelectedFile(url: URL(fileURLWithPath: "/test.pdf"), name: "File_name_one.pdf", size: 364000, uploadStatus: .success),
                SelectedFile(url: URL(fileURLWithPath: "/test2.pdf"), name: "File_name_two.pdf", size: 12000000, uploadStatus: .uploading),
                SelectedFile(url: URL(fileURLWithPath: "/test3.pdf"), name: "File_name_three.pdf", size: 364000, uploadStatus: .error)
            ],
            onDelete: { _ in }
        )
    }
}
