import Foundation

struct Constants {
    
    // MARK: - API Configuration
    
    /// Base URL for backend API
    /// - For iOS Simulator: Use localhost
    /// - For Physical Device: Use your Mac's IP address (find with: ifconfig | grep inet)
    static let apiBaseURL: String = {
        #if targetEnvironment(simulator)
        return "http://localhost:8000"
        #else
        // TODO: Replace with your Mac's IP address when testing on physical device
        // Example: "http://192.168.1.100:8000"
        return "http://localhost:8000"
        #endif
    }()
    
    // MARK: - API Endpoints
    
    struct Endpoints {
        static let documents = "/api/documents"
        static let podcasts = "/api/podcasts"
        static let questions = "/api/questions"
        
        static let health = "/"
        static let uploadDocument = "/api/documents/upload"
        static let generatePodcast = "/api/podcasts/generate"
        static let askQuestion = "/api/questions/ask"
    }
    
    // MARK: - App Configuration
    
    /// Maximum file size for PDF uploads (in bytes)
    /// 10 MB = 10 * 1024 * 1024
    static let maxFileSize: Int = 10_485_760
    
    /// Supported file types
    static let supportedFileTypes = ["pdf"]
    
    // MARK: - UI Configuration
    
    /// Default corner radius for cards and buttons
    static let cornerRadius: CGFloat = 12
    
    /// Standard padding
    static let padding: CGFloat = 16
}
