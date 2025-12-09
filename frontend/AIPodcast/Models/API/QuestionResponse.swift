import Foundation

struct QuestionResponse: Codable, Sendable {
    let answerAudioUrl: String
    let answerText: String
    let sources: [String]
    let usedWebSearch: Bool
    
    enum CodingKeys: String, CodingKey {
        case answerAudioUrl = "answer_audio_url"
        case answerText = "answer_text"
        case sources
        case usedWebSearch = "used_web_search"
    }
}
