import SwiftUI

struct EmptyStateView: View {
    let icon: String
    let title: String
    let message: String
    let actionTitle: String?
    let action: (() -> Void)?
    
    init(
        icon: String,
        title: String,
        message: String,
        actionTitle: String? = nil,
        action: (() -> Void)? = nil
    ) {
        self.icon = icon
        self.title = title
        self.message = message
        self.actionTitle = actionTitle
        self.action = action
    }
    
    var body: some View {
        VStack(spacing: Spacing.lg) {
            Spacer()
            
            // Icon
            Image(systemName: icon)
                .font(.system(size: 60))
                .foregroundColor(.appSecondaryText)
                .padding(.bottom, Spacing.sm)
            
            // Title
            Text(title)
                .font(.appTitle2)
                .fontWeight(.bold)
                .foregroundColor(.appText)
                .multilineTextAlignment(.center)
            
            // Message
            Text(message)
                .font(.appBody)
                .foregroundColor(.appSecondaryText)
                .multilineTextAlignment(.center)
                .padding(.horizontal, Spacing.xl)
            
            // Action Button (optional)
            if let actionTitle = actionTitle, let action = action {
                Button(action: action) {
                    Text(actionTitle)
                        .font(.appBodyBold)
                        .foregroundColor(.white)
                        .padding(.horizontal, Spacing.xl)
                        .padding(.vertical, Spacing.md)
                        .background(Color.appPrimary)
                        .cornerRadius(CornerRadius.md)
                }
                .padding(.top, Spacing.sm)
            }
            
            Spacer()
        }
        .frame(maxWidth: .infinity, maxHeight: .infinity)
    }
}

// MARK: - Compact Empty State (for smaller spaces)
struct CompactEmptyStateView: View {
    let icon: String
    let message: String
    
    var body: some View {
        VStack(spacing: Spacing.md) {
            Image(systemName: icon)
                .font(.system(size: 40))
                .foregroundColor(.appTertiaryText)
            
            Text(message)
                .font(.appCallout)
                .foregroundColor(.appSecondaryText)
                .multilineTextAlignment(.center)
        }
        .padding(Spacing.xl)
    }
}

// MARK: - Predefined Empty States
extension EmptyStateView {
    // No Documents
    static func noDocuments(action: @escaping () -> Void) -> EmptyStateView {
        EmptyStateView(
            icon: "doc.text",
            title: "No Documents",
            message: "Upload your first document to get started generating podcasts.",
            actionTitle: "Upload Document",
            action: action
        )
    }
    
    // No Podcasts
    static func noPodcasts(action: @escaping () -> Void) -> EmptyStateView {
        EmptyStateView(
            icon: "waveform",
            title: "No Podcasts Yet",
            message: "Generate your first podcast from uploaded documents.",
            actionTitle: "Generate Podcast",
            action: action
        )
    }
    
    // No Downloads
    static var noDownloads: EmptyStateView {
        EmptyStateView(
            icon: "arrow.down.circle",
            title: "No Downloads",
            message: "Podcasts you download will appear here for offline listening."
        )
    }
    
    // No Search Results
    static func noSearchResults(query: String) -> EmptyStateView {
        EmptyStateView(
            icon: "magnifyingglass",
            title: "No Results",
            message: "We couldn't find anything matching \"\(query)\". Try a different search."
        )
    }
    
    // Network Error
    static func networkError(retry: @escaping () -> Void) -> EmptyStateView {
        EmptyStateView(
            icon: "wifi.slash",
            title: "Connection Error",
            message: "Unable to connect to the server. Please check your internet connection and try again.",
            actionTitle: "Retry",
            action: retry
        )
    }
    
    // Generic Error
    static func error(message: String, retry: (() -> Void)? = nil) -> EmptyStateView {
        EmptyStateView(
            icon: "exclamationmark.triangle",
            title: "Something Went Wrong",
            message: message,
            actionTitle: retry != nil ? "Try Again" : nil,
            action: retry
        )
    }
}

// MARK: - Previews
#Preview("Empty States - Light Mode") {
    ScrollView {
        VStack(spacing: Spacing.xxl) {
            EmptyStateView.noDocuments(action: {})
                .frame(height: 400)
            
            Divider()
            
            EmptyStateView.noPodcasts(action: {})
                .frame(height: 400)
            
            Divider()
            
            EmptyStateView.noDownloads
                .frame(height: 400)
        }
    }
}

#Preview("Empty States - Dark Mode") {
    ScrollView {
        VStack(spacing: Spacing.xxl) {
            EmptyStateView.networkError(retry: {})
                .frame(height: 400)
            
            Divider()
            
            EmptyStateView.noSearchResults(query: "American History")
                .frame(height: 400)
        }
    }
    .preferredColorScheme(.dark)
}

#Preview("Compact Empty State") {
    VStack {
        CompactEmptyStateView(
            icon: "folder",
            message: "This folder is empty"
        )
        
        Divider()
        
        CompactEmptyStateView(
            icon: "star",
            message: "No favorites yet"
        )
    }
}

#Preview("Custom Empty State") {
    EmptyStateView(
        icon: "book.closed",
        title: "Welcome to Your Library",
        message: "Start building your collection by uploading documents and generating podcasts.",
        actionTitle: "Get Started",
        action: {}
    )
}
