import SwiftUI

struct DocumentCard: View {
    let filename: String
    let uploadDate: Date
    let status: DocumentStatus
    let fileSize: String?
    let onTap: () -> Void
    let onDelete: () -> Void
    
    enum DocumentStatus {
        case uploading(progress: Double) // 0.0 to 1.0
        case ready
        case failed
        
        var color: Color {
            switch self {
            case .uploading:
                return .appWarning
            case .ready:
                return .appSuccess
            case .failed:
                return .appError
            }
        }
        
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
        Button(action: onTap) {
            HStack(spacing: Spacing.md) {
                // Document Icon with Progress Overlay
                ZStack {
                    Image(systemName: status.documentIcon)
                        .font(.title2)
                        .foregroundColor(.white)
                        .frame(width: 44, height: 44)
                        .clipShape(RoundedRectangle(cornerRadius: CornerRadius.sm))
                        .glassEffect(.clear, in: Circle())
                    
                    // Circular Progress Overlay (only for uploading)
                    if case .uploading(let progress) = status {
                        CircularProgressView(progress: progress)
                            .frame(width: 44, height: 44)
                    }
                }
                
                // Document Info
                VStack(alignment: .leading, spacing: Spacing.xs) {
                    Text(filename)
                        .font(.appCallout)
                        .fontWeight(.medium)
                        .foregroundColor(.white)
                        .lineLimit(1)
                    
                    HStack(spacing: Spacing.sm) {
                        Text(formattedDate)
                            .font(.appCaption)
                            .foregroundColor(.white.opacity(0.7))
                        
                        if let size = fileSize {
                            Text("•")
                                .foregroundColor(.white.opacity(0.5))
                            Text(size)
                                .font(.appCaption)
                                .foregroundColor(.white.opacity(0.7))
                        }
                    }
                }
                
                Spacer()
                
                // Right side: File size + Delete OR Failed badge
                if case .failed = status {
                    // Show failed badge
                    HStack(spacing: Spacing.xs) {
                        Image(systemName: "xmark")
                            .font(.appCaption)
                            .fontWeight(.semibold)
                        Text("Failed")
                            .font(.appCaption)
                            .fontWeight(.medium)
                    }
                    .foregroundColor(.appError)
                    .padding(.horizontal, Spacing.sm)
                    .padding(.vertical, Spacing.xs)
                    .background(Color.appError.opacity(0.15))
                    .clipShape(RoundedRectangle(cornerRadius: CornerRadius.sm))
                    .glassEffect(.clear, in: RoundedRectangle(cornerRadius: CornerRadius.sm))
                } else {
                    // Show file size and delete button
                    HStack(spacing: Spacing.md) {
                        if let size = fileSize {
                            Text(size)
                                .font(.appCaption)
                                .foregroundColor(.white.opacity(0.7))
                        }
                        
                        Button(action: onDelete) {
                            Image(systemName: "trash.fill")
                        }
                        .buttonStyle(BareIconButtonStyle(size: .large))
                    }
                }
            }
        }
    }
    
    private var formattedDate: String {
        let formatter = RelativeDateTimeFormatter()
        formatter.unitsStyle = .abbreviated
        return formatter.localizedString(for: uploadDate, relativeTo: Date())
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
                    Color.white.opacity(0.2),
                    lineWidth: 3
                )
            
            // Progress circle
            Circle()
                .trim(from: 0, to: progress)
                .stroke(
                    Color.appWarning,
                    style: StrokeStyle(
                        lineWidth: 3,
                        lineCap: .round
                    )
                )
                .rotationEffect(.degrees(-90))
                .animation(.easeInOut(duration: 0.3), value: progress)
        }
    }
}

// MARK: Previews
#Preview("Document Cards - Dark Mode") {
    ZStack {
        LinearGradient(
            colors: [
                Color.blue.opacity(0.2),
                Color.indigo.opacity(0.2),
                Color.black.opacity(0.1)
            ],
            startPoint: .topLeading,
            endPoint: .bottomTrailing
        )
        .ignoresSafeArea()
        
        VStack(spacing: Spacing.md) {
            Text("Document Cards")
                .font(.appTitle)
                .foregroundColor(.white)
                .padding(.bottom, Spacing.sm)
            
            DocumentCard(
                filename: "New Employee Onboarding",
                uploadDate: Date().addingTimeInterval(-3600),
                status: .ready,
                fileSize: "2.4 MB",
                onTap: {},
                onDelete: {}
            )
            
            DocumentCard(
                filename: "Installing Python on macOS",
                uploadDate: Date().addingTimeInterval(-300),
                status: .uploading(progress: 0.35),
                fileSize: "5.1 MB",
                onTap: {},
                onDelete: {}
            )
            
            DocumentCard(
                filename: "Development Onboarding",
                uploadDate: Date().addingTimeInterval(-120),
                status: .uploading(progress: 0.75),
                fileSize: "1.8 MB",
                onTap: {},
                onDelete: {}
            )
            
            DocumentCard(
                filename: "Getting Started - SWE",
                uploadDate: Date().addingTimeInterval(-600),
                status: .failed,
                fileSize: "3.2 MB",
                onTap: {},
                onDelete: {}
            )
        }
        .padding()
        .preferredColorScheme(.dark)
    }
}
