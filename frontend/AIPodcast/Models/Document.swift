import Foundation

struct Document: Codable, Identifiable {
    let id: String
    let filename: String
    let uploadedAt: Date
    let status: DocumentStatus
    
    enum DocumentStatus: String, Codable {
        case uploading
        case processing
        case ready
        case failed
    }
    
    enum CodingKeys: String, CodingKey {
        case id
        case filename
        case uploadedAt = "uploaded_at"
        case status
    }
}
