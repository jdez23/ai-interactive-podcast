import Foundation

struct DocumentUploadResponse: Codable, Sendable {
    let documentId: String
    let filename: String
    let status: String
    let chunksCount: Int
    
    enum CodingKeys: String, CodingKey {
        case documentId = "document_id"
        case filename
        case status
        case chunksCount = "chunks_count"
    }
}
