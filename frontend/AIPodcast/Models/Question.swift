import Foundation

struct Question: Codable, Identifiable {
    let id: String
    let podcastId: String
    let questionText: String
    let answerText: String?
    let answerAudioUrl: String?
    let timestamp: Int
    let createdAt: Date
    
    enum CodingKeys: String, CodingKey {
        case id
        case podcastId = "podcast_id"
        case questionText = "question_text"
        case answerText = "answer_text"
        case answerAudioUrl = "answer_audio_url"
        case timestamp
        case createdAt = "created_at"
    }
}
