import SwiftUI

struct PodcastCard: View {
    let title: String
    let subtitle: String?
    let duration: Int?
    let thumbnailIcon: String
    let onTap: () -> Void
    let onPlayTap: (() -> Void)?
    
    init(
        title: String,
        subtitle: String? = nil,
        duration: Int? = nil,
        thumbnailIcon: String = "waveform",
        onTap: @escaping () -> Void,
        onPlayTap: (() -> Void)? = nil
    ) {
        self.title = title
        self.subtitle = subtitle
        self.duration = duration
        self.thumbnailIcon = thumbnailIcon
        self.onTap = onTap
        self.onPlayTap = onPlayTap
    }
    
    var body: some View {
        Button(action: onTap) {
            HStack(spacing: Spacing.md) {
                // Thumbnail
                ZStack {
                    RoundedRectangle(cornerRadius: CornerRadius.md)
                        .fill(
                            LinearGradient(
                                colors: [Color.appPrimary.opacity(0.8), Color.appAccent.opacity(0.6)],
                                startPoint: .topLeading,
                                endPoint: .bottomTrailing
                            )
                        )
                        .frame(width: 60, height: 60)
                    
                    Image(systemName: thumbnailIcon)
                        .font(.title3)
                        .foregroundColor(.white)
                }
                
                // Podcast Info
                VStack(alignment: .leading, spacing: Spacing.xs) {
                    Text(title)
                        .font(.appCallout)
                        .fontWeight(.semibold)
                        .foregroundColor(.appText)
                        .lineLimit(2)
                    
                    if let subtitle = subtitle {
                        Text(subtitle)
                            .font(.appCaption)
                            .foregroundColor(.appSecondaryText)
                            .lineLimit(1)
                    }
                    
                    if let duration = duration {
                        HStack(spacing: Spacing.xs) {
                            Image(systemName: "clock")
                                .font(.appCaption2)
                            Text(formattedDuration)
                                .font(.appCaption)
                        }
                        .foregroundColor(.appTertiaryText)
                    }
                }
                
                Spacer()
                
                // Play Button
                if let playAction = onPlayTap {
                    Button(action: playAction) {
                        Image(systemName: "play.circle.fill")
                            .font(.title)
                            .foregroundColor(.appPrimary)
                    }
                    .buttonStyle(PlainButtonStyle())
                }
            }
            .padding(Spacing.md)
            .background(Color.appCardBackground)
            .cornerRadius(CornerRadius.md)
            .appLightShadow()
        }
        .buttonStyle(PlainButtonStyle())
    }
    
    private var formattedDuration: String {
        guard let duration = duration else { return "--:--" }
        let minutes = duration / 60
        let seconds = duration % 60
        return String(format: "%d:%02d", minutes, seconds)
    }
}

// MARK: - Large Podcast Card (for featured content)
struct LargePodcastCard: View {
    let title: String
    let subtitle: String?
    let duration: Int?
    let thumbnailIcon: String
    let onTap: () -> Void
    
    init(
        title: String,
        subtitle: String? = nil,
        duration: Int? = nil,
        thumbnailIcon: String = "waveform",
        onTap: @escaping () -> Void
    ) {
        self.title = title
        self.subtitle = subtitle
        self.duration = duration
        self.thumbnailIcon = thumbnailIcon
        self.onTap = onTap
    }
    
    var body: some View {
        Button(action: onTap) {
            VStack(alignment: .leading, spacing: Spacing.sm) {
                // Large Thumbnail
                ZStack {
                    RoundedRectangle(cornerRadius: CornerRadius.lg)
                        .fill(
                            LinearGradient(
                                colors: [Color.appPrimary.opacity(0.8), Color.appAccent.opacity(0.6)],
                                startPoint: .topLeading,
                                endPoint: .bottomTrailing
                            )
                        )
                        .frame(width: 160, height: 160)
                    
                    Image(systemName: thumbnailIcon)
                        .font(.system(size: 50))
                        .foregroundColor(.white)
                }
                
                // Info
                VStack(alignment: .leading, spacing: Spacing.xs) {
                    Text(title)
                        .font(.appCallout)
                        .fontWeight(.semibold)
                        .foregroundColor(.appText)
                        .lineLimit(2)
                        .frame(width: 160, alignment: .leading)
                    
                    if let subtitle = subtitle {
                        Text(subtitle)
                            .font(.appCaption)
                            .foregroundColor(.appSecondaryText)
                            .lineLimit(1)
                            .frame(width: 160, alignment: .leading)
                    }
                    
                    if let duration = duration {
                        HStack(spacing: Spacing.xs) {
                            Image(systemName: "clock")
                                .font(.appCaption2)
                            Text(formattedDuration)
                                .font(.appCaption)
                        }
                        .foregroundColor(.appTertiaryText)
                    }
                }
            }
        }
        .buttonStyle(PlainButtonStyle())
    }
    
    private var formattedDuration: String {
        guard let duration = duration else { return "--:--" }
        let minutes = duration / 60
        let seconds = duration % 60
        return String(format: "%d:%02d", minutes, seconds)
    }
}

// MARK: - Previews
#Preview("Podcast Cards - Light Mode") {
    ScrollView {
        VStack(spacing: Spacing.lg) {
            Text("Standard Cards")
                .font(.appTitle3)
                .frame(maxWidth: .infinity, alignment: .leading)
            
            VStack(spacing: Spacing.md) {
                PodcastCard(
                    title: "New Employee Onboarding",
                    subtitle: "Generated from 8 documents",
                    duration: 180,
                    onTap: {},
                    onPlayTap: {}
                )
                
                PodcastCard(
                    title: "Installing Python on macOS",
                    subtitle: "Python at Apple",
                    duration: 600,
                    onTap: {},
                    onPlayTap: {}
                )
                
                PodcastCard(
                    title: "Development Onboarding",
                    duration: 240,
                    onTap: {},
                    onPlayTap: nil
                )
            }
            
            Text("Large Cards")
                .font(.appTitle3)
                .frame(maxWidth: .infinity, alignment: .leading)
                .padding(.top)
            
            ScrollView(.horizontal, showsIndicators: false) {
                HStack(spacing: Spacing.md) {
                    LargePodcastCard(
                        title: "Getting Started - SWE",
                        subtitle: "New Employee Onboarding",
                        duration: 420,
                        onTap: {}
                    )
                    
                    LargePodcastCard(
                        title: "About Apple JDK",
                        subtitle: "Java at Apple",
                        duration: 300,
                        onTap: {}
                    )
                    
                    LargePodcastCard(
                        title: "Ethics and Comliance",
                        duration: 540,
                        onTap: {}
                    )
                }
            }
        }
        .padding()
    }
}

#Preview("Podcast Cards - Dark Mode") {
    VStack(spacing: Spacing.md) {
        PodcastCard(
            title: "New Employee Onboarding",
            subtitle: "Generated from 8 documents",
            duration: 180,
            onTap: {},
            onPlayTap: {}
        )
        
        PodcastCard(
            title: "Installing Python on macOS",
            subtitle: "Python at Apple",
            duration: 600,
            onTap: {},
            onPlayTap: {}
        )
    }
    .padding()
    .preferredColorScheme(.dark)
}
