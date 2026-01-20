import Foundation

struct QuestionRequest: Codable, Sendable {
    let podcastId: String
    let question: String
    let timestamp: Double
    
    enum CodingKeys: String, CodingKey {
        case podcastId = "podcast_id"
        case question
        case timestamp
    }
}
