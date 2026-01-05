import Foundation
import Alamofire

enum APIError: Error, LocalizedError {
    case invalidURL
    case networkError(Error)
    case decodingError(Error)
    case serverError(statusCode: Int, message: String?)
    case invalidResponse
    case fileNotFound
    
    var errorDescription: String? {
        switch self {
        case .invalidURL:
            return "Invalid URL"
        case .networkError(let error):
            return "Network error: \(error.localizedDescription)"
        case .decodingError(let error):
            return "Failed to decode response: \(error.localizedDescription)"
        case .serverError(let statusCode, let message):
            return "Server error (\(statusCode)): \(message ?? "Unknown error")"
        case .invalidResponse:
            return "Invalid response from server"
        case .fileNotFound:
            return "File not found"
        }
    }
}

@MainActor
class APIService {
    static let shared = APIService()
    private let baseURL = Constants.apiBaseURL
    
    private init() {}
    
    // MARK: - Health Check
    
    func healthCheck() async throws -> [String: String] {
        let url = "\(baseURL)\(Constants.Endpoints.health)"
        
        let data = try await AF.request(url, method: .get)
            .validate()
            .serializingData()
            .value
        
        let decoder = JSONDecoder()
        return try decoder.decode([String: String].self, from: data)
    }
    
    // MARK: - Documents
    
    func uploadDocument(fileURL: URL) async throws -> Document {
        guard FileManager.default.fileExists(atPath: fileURL.path) else {
            throw APIError.fileNotFound
        }
        
        let url = "\(baseURL)\(Constants.Endpoints.uploadDocument)"
        
        let data = try await AF.upload(
            multipartFormData: { multipartFormData in
                multipartFormData.append(fileURL, withName: "file")
            },
            to: url
        )
        .validate()
        .serializingData()
        .value
        
        let decoder = JSONDecoder()
        let uploadResponse = try decoder.decode(DocumentUploadResponse.self, from: data)
        
        // Convert API response to app's Document model
        return Document(
            id: uploadResponse.documentId,
            filename: uploadResponse.filename,
            uploadedAt: Date(),
            status: uploadResponse.status == "processed" ? .ready : .processing
        )
    }
    
    // MARK: - Podcasts

    func generatePodcast(documentIds: [String], topic: String, durationMinutes: Int) async throws -> Podcast {
        let url = "\(baseURL)\(Constants.Endpoints.generatePodcast)"
        
        let request = PodcastGenerateRequest(
            documentIds: documentIds,
            topic: topic,
            durationMinutes: durationMinutes
        )
        
        let encoder = JSONEncoder()
        let requestData = try encoder.encode(request)
        
        var urlRequest = URLRequest(url: URL(string: url)!)
        urlRequest.httpMethod = "POST"
        urlRequest.setValue("application/json", forHTTPHeaderField: "Content-Type")
        urlRequest.httpBody = requestData
        
        let data = try await AF.request(urlRequest)
            .validate()
            .serializingData()
            .value
        
        let decoder = JSONDecoder()
        let generateResponse = try decoder.decode(PodcastGenerateResponse.self, from: data)
        
        // Convert API response to app's Podcast model
        return Podcast(
            id: generateResponse.podcastId,
            documentIds: documentIds,
            audioUrl: generateResponse.audioUrl,
            duration: generateResponse.durationSeconds,
            status: .ready,
            createdAt: Date()
        )
    }

    func getPodcastStatus(podcastId: String) async throws -> Podcast {
        let url = "\(baseURL)/api/podcasts/\(podcastId)"
        
        let data = try await AF.request(url, method: .get)
            .validate()
            .serializingData()
            .value
        
        let decoder = JSONDecoder()
        let statusResponse = try decoder.decode(PodcastStatusResponse.self, from: data)
        
        // Convert API response to app's Podcast model
        return Podcast(
            id: statusResponse.podcastId,
            documentIds: [], // Not provided in status response
            audioUrl: statusResponse.audioUrl,
            duration: statusResponse.durationSeconds ?? 0,
            status: statusResponse.status == "complete" ? .ready : .generating,
            createdAt: Date()
        )
    }

    // MARK: - Questions
    
    func askQuestion(podcastId: String, questionText: String) async throws -> Question {
        let url = "\(baseURL)\(Constants.Endpoints.askQuestion)"
        
        let request = QuestionRequest(
            podcastId: podcastId,
            question: questionText
        )
        
        let encoder = JSONEncoder()
        let requestData = try encoder.encode(request)
        
        var urlRequest = URLRequest(url: URL(string: url)!)
        urlRequest.httpMethod = "POST"
        urlRequest.setValue("application/json", forHTTPHeaderField: "Content-Type")
        urlRequest.httpBody = requestData
        
        let data = try await AF.request(urlRequest)
            .validate()
            .serializingData()
            .value
        
        let decoder = JSONDecoder()
        let questionResponse = try decoder.decode(QuestionResponse.self, from: data)
        
        // Convert API response to app's Question model
        return Question(
            id: UUID().uuidString,
            podcastId: podcastId,
            questionText: questionText,
            answerText: questionResponse.answerText,
            answerAudioUrl: questionResponse.answerAudioUrl,
            timestamp: 0,
            createdAt: Date()
        )
    }
}
