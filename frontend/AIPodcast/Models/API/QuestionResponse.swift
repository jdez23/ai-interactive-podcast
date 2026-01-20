import Foundation

struct QuestionResponse: Codable, Sendable {
    let answerText: String
    let answerOnly: String?
    let audioUrl: String?
    let sources: [String]
    let contextUsed: ContextUsed
    let timestamp: Double
    
    struct ContextUsed: Codable, Sendable {
        let documentChunks: Int
        let dialogueExchanges: Int
        
        enum CodingKeys: String, CodingKey {
            case documentChunks = "document_chunks"
            case dialogueExchanges = "dialogue_exchanges"
        }
    }
    
    enum CodingKeys: String, CodingKey {
        case answerText = "answer_text"
        case answerOnly = "answer_only"
        case audioUrl = "audio_url"
        case sources
        case contextUsed = "context_used"
        case timestamp
    }
}
