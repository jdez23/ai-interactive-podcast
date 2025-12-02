import XCTest
@testable import AIPodcast

final class ModelTests: XCTestCase {

    private var jsonEncoder: JSONEncoder!
    private var jsonDecoder: JSONDecoder!
    private var iso8601Formatter: ISO8601DateFormatter!

    override func setUpWithError() throws {
        try super.setUpWithError()
        iso8601Formatter = ISO8601DateFormatter()
        iso8601Formatter.formatOptions = [.withInternetDateTime, .withFractionalSeconds]
        
        jsonEncoder = JSONEncoder()
        // Use a custom encoding strategy
        jsonEncoder.dateEncodingStrategy = .custom { (date, encoder) in
            var container = encoder.singleValueContainer()
            let dateString = self.iso8601Formatter.string(from: date)
            try container.encode(dateString)
        }
        
        jsonDecoder = JSONDecoder()
        // Use a custom decoding strategy
        jsonDecoder.dateDecodingStrategy = .custom { (decoder) -> Date in
            let container = try decoder.singleValueContainer()
            let dateString = try container.decode(String.self)
            guard let date = self.iso8601Formatter.date(from: dateString) else {
                throw DecodingError.dataCorruptedError(in: container, debugDescription: "Cannot decode date string \(dateString)")
            }
            return date
        }
    }

    override func tearDownWithError() throws {
        jsonEncoder = nil
        jsonDecoder = nil
        iso8601Formatter = nil
        try super.tearDownWithError()
    }

    func testDocumentEncodingAndDecoding() throws {
        // 1. Create a test instance of Document
        let originalDate = Date()
        let document = Document(
            id: "doc123",
            filename: "MyReport.pdf",
            uploadedAt: originalDate,
            status: .ready
        )

        // 2. Encode the Document to JSON data
        let encodedData = try jsonEncoder.encode(document)

        // 3. Decode the JSON data back into a Document instance
        let decodedDocument = try jsonDecoder.decode(Document.self, from: encodedData)

        // 4. Verify that the original and decoded values match
        XCTAssertEqual(decodedDocument.id, document.id, "ID should match")
        XCTAssertEqual(decodedDocument.filename, document.filename, "Filename should match")
        
        // Compare dates with a small tolerance due to potential precision differences in encoding/decoding
        XCTAssertEqual(decodedDocument.uploadedAt.timeIntervalSince1970, document.uploadedAt.timeIntervalSince1970, accuracy: 0.1, "UploadedAt date should match")
        
        XCTAssertEqual(decodedDocument.status, document.status, "Status should match")

        // To explicitly check snake_case in the JSON:
        let jsonObject = try JSONSerialization.jsonObject(with: encodedData, options: []) as? [String: Any]
        XCTAssertNotNil(jsonObject, "Encoded data should be a JSON object")
        XCTAssertEqual(jsonObject?["id"] as? String, document.id)
        XCTAssertEqual(jsonObject?["filename"] as? String, document.filename)
        XCTAssertNotNil(jsonObject?["uploaded_at"], "JSON should contain 'uploaded_at' key")
        XCTAssertEqual(jsonObject?["status"] as? String, document.status.rawValue)
    }
    
    func testPodcastEncodingAndDecoding() throws {
        // 1. Create a test instance of Podcast
        let originalDate = Date()
        let podcast = Podcast(
            id: "pod456",
            documentIds: ["doc123", "doc456"],
            audioUrl: "https://example.com/audio.mp3",
            duration: 3600, // 1 hour in seconds
            status: .ready,
            createdAt: originalDate
        )

        // 2. Encode the Podcast to JSON data
        let encodedData = try jsonEncoder.encode(podcast)

        // 3. Decode the JSON data back into a Podcast instance
        let decodedPodcast = try jsonDecoder.decode(Podcast.self, from: encodedData)

        // 4. Verify that the original and decoded values match
        XCTAssertEqual(decodedPodcast.id, podcast.id, "ID should match")
        XCTAssertEqual(decodedPodcast.documentIds, podcast.documentIds, "Document IDs should match")
        XCTAssertEqual(decodedPodcast.audioUrl, podcast.audioUrl, "Audio URL should match")
        XCTAssertEqual(decodedPodcast.duration, podcast.duration, "Duration should match")
        XCTAssertEqual(decodedPodcast.status, podcast.status, "Status should match")
        XCTAssertEqual(decodedPodcast.createdAt.timeIntervalSince1970, podcast.createdAt.timeIntervalSince1970, accuracy: 0.1, "CreatedAt date should match")

        // Verify CodingKeys by checking the raw JSON structure
        let jsonObject = try JSONSerialization.jsonObject(with: encodedData, options: []) as? [String: Any]
        XCTAssertNotNil(jsonObject, "Encoded data should be a JSON object")
        XCTAssertEqual(jsonObject?["id"] as? String, podcast.id)
        XCTAssertNotNil(jsonObject?["document_ids"], "JSON should contain 'document_ids' key")
        XCTAssertEqual(jsonObject?["audio_url"] as? String, podcast.audioUrl)
        XCTAssertEqual(jsonObject?["duration"] as? Int, podcast.duration)
        XCTAssertEqual(jsonObject?["status"] as? String, podcast.status.rawValue)
        XCTAssertNotNil(jsonObject?["created_at"], "JSON should contain 'created_at' key")
    }
    
    func testQuestionEncodingAndDecoding() throws {
        // 1. Create a test instance of Question
        let originalDate = Date()
        let question = Question(
            id: "q789",
            podcastId: "pod456",
            questionText: "What is the main topic of this podcast?",
            answerText: "The main topic is Swift concurrency.",
            answerAudioUrl: "https://example.com/answer_audio.mp3",
            timestamp: 120, // 2 minutes into the podcast
            createdAt: originalDate
        )

        // 2. Encode the Question to JSON data
        let encodedData = try jsonEncoder.encode(question)

        // 3. Decode the JSON data back into a Question instance
        let decodedQuestion = try jsonDecoder.decode(Question.self, from: encodedData)

        // 4. Verify that the original and decoded values match
        XCTAssertEqual(decodedQuestion.id, question.id, "ID should match")
        XCTAssertEqual(decodedQuestion.podcastId, question.podcastId, "Podcast ID should match")
        XCTAssertEqual(decodedQuestion.questionText, question.questionText, "Question text should match")
        XCTAssertEqual(decodedQuestion.answerText, question.answerText, "Answer text should match")
        XCTAssertEqual(decodedQuestion.answerAudioUrl, question.answerAudioUrl, "Answer audio URL should match")
        XCTAssertEqual(decodedQuestion.timestamp, question.timestamp, "Timestamp should match")
        XCTAssertEqual(decodedQuestion.createdAt.timeIntervalSince1970, question.createdAt.timeIntervalSince1970, accuracy: 0.1, "CreatedAt date should match")

        // Verify CodingKeys by checking the raw JSON structure
        let jsonObject = try JSONSerialization.jsonObject(with: encodedData, options: []) as? [String: Any]
        XCTAssertNotNil(jsonObject, "Encoded data should be a JSON object")
        XCTAssertEqual(jsonObject?["id"] as? String, question.id)
        XCTAssertEqual(jsonObject?["podcast_id"] as? String, question.podcastId)
        XCTAssertEqual(jsonObject?["question_text"] as? String, question.questionText)
        XCTAssertEqual(jsonObject?["answer_text"] as? String, question.answerText)
        XCTAssertEqual(jsonObject?["answer_audio_url"] as? String, question.answerAudioUrl)
        XCTAssertEqual(jsonObject?["timestamp"] as? Int, question.timestamp)
        XCTAssertNotNil(jsonObject?["created_at"], "JSON should contain 'created_at' key")
    }


}
