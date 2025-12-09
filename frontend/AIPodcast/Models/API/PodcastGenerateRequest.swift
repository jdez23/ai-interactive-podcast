import Foundation

struct PodcastGenerateRequest: Codable, Sendable {
    let documentIds: [String]
    let topic: String
    let durationMinutes: Int
    
    enum CodingKeys: String, CodingKey {
        case documentIds = "document_ids"
        case topic
        case durationMinutes = "duration_minutes"
    }
}
