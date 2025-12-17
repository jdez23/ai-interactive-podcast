import SwiftUI

struct DocumentCard: View {
    let filename: String
    let uploadDate: Date
    let status: DocumentStatus
    let fileSize: String?
    let onTap: () -> Void
    
    enum DocumentStatus {
        case uploading
        case processing
        case ready
        case failed
        
        var color: Color {
            switch self {
            case .uploading, .processing:
                return .appWarning
                
            case .ready:
                return .appSuccess
                
            case .failed:
                return .appError
            }
        }
        
        var icon: String {
            switch self {
            case .uploading:
                return "arrow.up.circle.fill"
            case .processing:
                return "gearshape.fill"
            case .ready:
                return "Ready"
            case .failed:
                return "Failed"
            }
        }
        
        var text: String {
            switch self {
            case .uploading:
                return "Uploading"
            case .processing:
                return "Processing"
            case .ready:
                return "Ready"
            case .failed:
                return "Failed"
            }
        }
    }
    
    var body: some View {
        Button(action: onTap) {
            HStack(spacing: Spacing.md) {
                // Document Icon
                Image(systemName: "text.document.fill")
                    .font(.title2)
                    .foregroundColor(.appPrimary)
                    .frame(width: 44, height: 44)
                    .background(Color.appPrimary.opacity(0.1))
                    .cornerRadius(CornerRadius.sm)
                
                // Document Info
                VStack(alignment: .leading, spacing: Spacing.xs) {
                    Text(filename)
                        .font(.appCallout)
                        .fontWeight(.medium)
                        .foregroundColor(.appText)
                        .lineLimit(1)
                    
                    HStack(spacing: Spacing.sm) {
                        Text(formattedDate)
                            .font(.appCaption)
                            .foregroundColor(.appSecondaryText)
                        
                        if let size = fileSize {
                            Text(".")
                                .foregroundColor(.appTertiaryText)
                            Text(size)
                                .font(.appCaption)
                                .foregroundColor(.appSecondaryText)
                        }
                    }
                }
                
                Spacer()
                
                // Status Badge
                HStack(spacing: Spacing.xs) {
                    Image(systemName: status.icon)
                        .font(.appCaption)
                    Text(status.text)
                        .font(.appCaption)
                }
                .foregroundColor(status.color)
                .padding(.horizontal, Spacing.sm)
                .padding(.vertical, Spacing.xs)
                .background(status.color.opacity(0.15))
                .cornerRadius(CornerRadius.sm)
            }
            .padding(Spacing.md)
            .background(Color.appCardBackground)
            .cornerRadius(CornerRadius.md)
            .appLightShadow()
        }
        .buttonStyle(PlainButtonStyle())
    }
    
    private var formattedDate: String {
        let formatter = RelativeDateTimeFormatter()
        formatter.unitsStyle = .abbreviated
        return formatter.localizedString(for: uploadDate, relativeTo: Date())
    }
}

// MARK: Previews
#Preview("Document Cards - Light Mode") {
    VStack(spacing: Spacing.md) {
        DocumentCard(
            filename:"New Employee Onboarding",
            uploadDate: Date().addingTimeInterval(-3600),
            status: .ready,
            fileSize: "2.4 MB",
            onTap: {}
        )
        
        DocumentCard(
            filename:"Installing Python on macOS",
            uploadDate: Date().addingTimeInterval(-7200),
            status: .processing,
            fileSize: "5.1 MB",
            onTap: {}
        )
        
        DocumentCard(
            filename:"Development Onboarding",
            uploadDate: Date().addingTimeInterval(-300),
            status: .uploading,
            fileSize: "1.8 MB",
            onTap: {}
        )
        
        DocumentCard(
            filename:"Getting Started - SWE",
            uploadDate: Date().addingTimeInterval(-600),
            status: .failed,
            fileSize: "3.2 MB",
            onTap: {}
        )
    }
    .padding()
}

#Preview("Document Cards - Dark Mode") {
    VStack(spacing: Spacing.md) {
        DocumentCard(
            filename:"New Employee Onboarding",
            uploadDate: Date().addingTimeInterval(-3600),
            status: .ready,
            fileSize: "2.4 MB",
            onTap: {}
        )
        
        DocumentCard(
            filename:"Installing Python on macOS",
            uploadDate: Date().addingTimeInterval(-7200),
            status: .processing,
            fileSize: "5.1 MB",
            onTap: {}
        )
    }
    .padding()
    .preferredColorScheme(.dark)
}
