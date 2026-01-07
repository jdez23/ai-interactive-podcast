import Foundation

struct PodcastGenerateResponse: Codable, Sendable {
    let podcastId: String
    let status: String
    let message: String
    
    enum CodingKeys: String, CodingKey {
        case podcastId = "podcast_id"
        case status
        case message
    }
}


struct PodcastStatusResponse: Codable, Sendable {
    let podcastId: String
    let status: String
    let createdAt: String
    let audioUrl: String?
    let scriptUrl: String?
    let durationSeconds: Double?
    let error: String?
    
    enum CodingKeys: String, CodingKey {
        case podcastId = "podcast_id"
        case status
        case createdAt = "created_at"
        case audioUrl = "audio_url"
        case scriptUrl = "script_url"
        case durationSeconds = "duration_seconds"
        case error
    }
}

