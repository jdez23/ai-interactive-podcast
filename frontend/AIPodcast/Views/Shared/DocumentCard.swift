import SwiftUI

struct DocumentCard: View {
    let filename: String
    let uploadDate: Date?
    let status: DocumentStatus
    let fileSize: String?
    let onTap: (() -> Void)?
    let onDelete: () -> Void
    
    // Convenience initializer for backward compatibility
    init(
        filename: String,
        uploadDate: Date,
        status: DocumentStatus,
        fileSize: String?,
        onTap: @escaping () -> Void,
        onDelete: @escaping () -> Void
    ) {
        self.filename = filename
        self.uploadDate = uploadDate
        self.status = status
        self.fileSize = fileSize
        self.onTap = onTap
        self.onDelete = onDelete
    }
    
    // Simple initializer without tap action
    init(
        filename: String,
        status: DocumentStatus,
        fileSize: String?,
        onDelete: @escaping () -> Void
    ) {
        self.filename = filename
        self.uploadDate = nil
        self.status = status
        self.fileSize = fileSize
        self.onTap = nil
        self.onDelete = onDelete
    }
    
    enum DocumentStatus {
        case uploading(progress: Double) // 0.0 to 1.0
        case ready
        case failed
        
        var documentIcon: String {
            switch self {
            case .uploading:
                return "doc.badge.arrow.up.fill"
            case .ready, .failed:
                return "doc.fill"
            }
        }
    }
    
    var body: some View {
        let content = HStack(spacing: 12) {
            // File Icon with Progress Overlay
            ZStack {
                Image(systemName: status.documentIcon)
                    .font(.system(size: 20))
                    .foregroundColor(.appPrimary)
                
                // Circular Progress Overlay (only for uploading)
                if case .uploading(let progress) = status {
                    CircularProgressView(progress: progress)
                        .frame(width: 32, height: 32)
                }
            }
            .frame(width: 32, height: 32)
            
            // File name
            VStack(alignment: .leading, spacing: 2) {
                Text(filename)
                    .font(.appBody)
                    .foregroundColor(.appText)
                    .lineLimit(1)
                
                // Show date only if provided (for library view)
                if let uploadDate = uploadDate {
                    Text(formattedDate(uploadDate))
                        .font(.appCaption)
                        .foregroundColor(.appSecondaryText)
                }
            }
            
            Spacer()
            
            // File size
            if let size = fileSize {
                Text(size)
                    .font(.appBody)
                    .foregroundColor(.appSecondaryText)  // Changed from .white
            }
            
            // Delete button (X)
            Button(action: onDelete) {
                Image(systemName: "xmark")
            }
            .buttonStyle(BareIconButtonStyle(tintColor: .appSecondaryText, size: .mini))
        }
        .padding(.vertical, 12)
        .padding(.horizontal, 16)
        .background(
            RoundedRectangle(cornerRadius: 8)
                .fill(Color.appSecondaryBackground)
        )
        
        // Wrap in button only if onTap is provided
        if let onTap = onTap {
            Button(action: onTap) {
                content
            }
            .buttonStyle(.plain)
        } else {
            content
        }
    }
    
    private func formattedDate(_ date: Date) -> String {
        let formatter = RelativeDateTimeFormatter()
        formatter.unitsStyle = .abbreviated
        return formatter.localizedString(for: date, relativeTo: Date())
    }
}

// MARK: - Circular Progress View
struct CircularProgressView: View {
    let progress: Double
    
    var body: some View {
        ZStack {
            // Background circle
            Circle()
                .stroke(
                    Color.appSecondaryText.opacity(0.3),
                    lineWidth: 2
                )
            
            // Progress circle
            Circle()
                .trim(from: 0, to: progress)
                .stroke(
                    Color.appOrange,
                    style: StrokeStyle(
                        lineWidth: 2,
                        lineCap: .round
                    )
                )
                .rotationEffect(.degrees(-90))
                .animation(.easeInOut(duration: 0.3), value: progress)
        }
    }
}

// MARK: Previews
#Preview("Document Cards - Light Mode") {
    ZStack {
        Color.appBackground.ignoresSafeArea()
        
        VStack(spacing: Spacing.md) {
            Text("Document Cards")
                .font(.appTitle)
                .foregroundColor(.appText)
                .padding(.bottom, Spacing.sm)
            
            DocumentCard(
                filename: "File_name_one.pdf",
                status: .ready,
                fileSize: "364 KB",
                onDelete: {}
            )
            
            DocumentCard(
                filename: "File_name_two.pdf",
                status: .uploading(progress: 0.65),
                fileSize: "12 MB",
                onDelete: {}
            )
            
            DocumentCard(
                filename: "File_name_three.pdf",
                status: .failed,
                fileSize: "364 KB",
                onDelete: {}
            )
        }
        .padding()
        .preferredColorScheme(.light)
    }
}
