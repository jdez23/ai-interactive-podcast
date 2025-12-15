import Foundation

struct Podcast: Codable, Identifiable {
    let id: String
    let documentIds: [String]
    let audioUrl: String?
    let duration: Int?
    let status: PodcastStatus
    let createdAt: Date
    var topic: String?
    
    enum PodcastStatus: String, Codable {
        case generating
        case ready
        case failed
    }
    
    enum CodingKeys: String, CodingKey {
        case id
        case documentIds = "document_ids"
        case audioUrl = "audio_url"
        case duration
        case status
        case createdAt = "created_at"
        case topic
    }
}
