import SwiftUI

struct FileListView: View {
    let files: [SelectedFile]
    let onDelete: (SelectedFile) -> Void
    
    var body: some View {
        ScrollView {
            VStack(spacing: 12) {
                ForEach(files) { file in
                    FileListItemView(file: file, onDelete: { onDelete(file) })
                }
            }
            .padding()
        }
    }
}

struct FileListItemView: View {
    let file: SelectedFile
    let onDelete: () -> Void
    
    var body: some View {
        HStack(spacing: 15) {
            // File Icon
            Image(systemName: "richtext.page.fill")
                .font(.title2)
                .foregroundColor(.blue)
            
            // File Info
            VStack(alignment: .leading, spacing: 4) {
                Text(file.name)
                    .font(.headline)
                    .lineLimit(1)
                
                HStack {
                    Text(file.sizeString)
                        .font(.caption)
                        .foregroundColor(.secondary)
                    
                    // Upload Status
                    if file.uploadStatus == .uploading {
                        ProgressView()
                            .scaleEffect(0.7)
                    } else if file.uploadStatus == .success {
                        Image(systemName: "checkmark.circle.fill")
                            .foregroundColor(.green)
                            .font(.caption)
                    } else if file.uploadStatus == .error {
                        Image(systemName: "exclamationmark.triangle.fill")
                            .foregroundColor(.red)
                            .font(.caption)
                    }
                }
            }
            
            Spacer()
            
            // Delete Button
            Button(action: onDelete) {
                Image(systemName: "trash.fill")
                    .foregroundColor(.red)
            }
        }
        .padding()
        .background(Color.gray.opacity(0.1))
        .cornerRadius(12)
    }
}

#Preview {
    FileListView(
        files: [
            SelectedFile(url: URL(fileURLWithPath: "/test.pdf"), name: "Test Document.pdf", size: 1024000),
            SelectedFile(url: URL(fileURLWithPath: "/test2.pdf"), name: "Another File.pdf", size: 2048000)
        ],
        onDelete: { _ in }
    )
    .padding()
}
