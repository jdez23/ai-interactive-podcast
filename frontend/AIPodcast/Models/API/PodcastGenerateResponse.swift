import Foundation

struct PodcastGenerateResponse: Codable, Sendable {
    let podcastId: String
    let audioUrl: String
    let script: String
    let durationSeconds: Int
    
    enum CodingKeys: String, CodingKey {
        case podcastId = "podcast_id"
        case audioUrl = "audio_url"
        case script
        case durationSeconds = "duration_seconds"
    }
}
