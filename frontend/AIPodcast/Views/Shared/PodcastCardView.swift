import SwiftUI

struct PodcastCardView: View {
    let podcast: Podcast
    
    var body: some View {
        VStack(alignment: .leading, spacing: 8) {
            // Thumbnail
            RoundedRectangle(cornerRadius: 12)
                .fill(Color.gray.opacity(0.3))
                .frame(width: 160, height: 160)
                .overlay(
                    Image(systemName: "waveform")
                        .font(.system(size: 40))
                        .foregroundColor(.white)
                )
            
            // Title
            Text(podcastTitle)
                .font(.headline)
                .lineLimit(2)
                .frame(width: 160, alignment: .leading)
            
            // Subtitle
            Text(podcastSubtitle)
                .font(.caption)
                .foregroundColor(.secondary)
                .lineLimit(1)
                .frame(width: 160, alignment: .leading)
        }
    }
    
    private var podcastTitle: String {
        // Extract topic from podcast or use default
        "Podcast Episode"
    }
    
    private var podcastSubtitle: String {
        if let duration = podcast.duration {
            return "\(duration / 60) min"
        }
        return "New"
    }
}

#Preview {
    PodcastCardView(podcast: Podcast(
        id: "test",
        documentIds: [],
        audioUrl: nil,
        duration: 180,
        status: .ready,
        progressPercentage: 100,
        createdAt: Date()
    ))
}
