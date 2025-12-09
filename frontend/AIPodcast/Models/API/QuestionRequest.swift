import Foundation

struct QuestionRequest: Codable, Sendable {
    let podcastId: String
    let question: String
    
    enum CodingKeys: String, CodingKey {
        case podcastId = "podcast_id"
        case question
    }
}
