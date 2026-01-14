import SwiftUI

struct LoadingOverlay: View {
    @State private var currentTipIndex = 0
    @State private var progress: CGFloat = 0.0
    
    let tips = [
        TipContent(
            icon: "doc.on.doc.fill",
            title: "Upload multiple documents",
            description: "Combine PDFs to create comprehensive podcast episodes on related topics"
        ),
        TipContent(
            icon: "book.fill",
            title: "Perfect for studying",
            description: "Turn your lecture notes and textbooks into engaging audio content"
        ),
        TipContent(
            icon: "headphones",
            title: "Learn on the go",
            description: "Listen to your personalized podcasts during commutes or workouts"
        ),
        TipContent(
            icon: "slider.horizontal.3",
            title: "Customize your learning",
            description: "Generate podcasts tailored to your specific materials and interests"
        ),
        TipContent(
            icon: "clock.fill",
            title: "Save time",
            description: "Transform hours of reading into digestible audio summaries"
        )
    ]
    
    var body: some View {
        ZStack {
            // Full black screen overlay
            Color.black
                .ignoresSafeArea()
            
            VStack(spacing: 0) {
                Spacer()
                
                // Carousel in the middle
                VStack(spacing: 24) {
                    // Icon
                    Image(systemName: tips[currentTipIndex].icon)
                        .font(.system(size: 60))
                        .foregroundColor(.blue)
                        .transition(.opacity)
                    
                    // Title
                    Text(tips[currentTipIndex].title)
                        .font(.title2)
                        .fontWeight(.bold)
                        .foregroundColor(.white)
                        .multilineTextAlignment(.center)
                        .transition(.opacity)
                    
                    // Description
                    Text(tips[currentTipIndex].description)
                        .font(.body)
                        .foregroundColor(.gray)
                        .multilineTextAlignment(.center)
                        .padding(.horizontal, 40)
                        .transition(.opacity)
                }
                .padding(.horizontal, 32)
                
                Spacer()
                
                // Progress bar at the bottom
                VStack(spacing: 12) {
                    Text("Generating your podcast...")
                        .font(.subheadline)
                        .foregroundColor(.white)
                    
                    GeometryReader { geometry in
                        ZStack(alignment: .leading) {
                            // Background
                            RoundedRectangle(cornerRadius: 10)
                                .fill(Color.gray.opacity(0.3))
                                .frame(height: 8)
                            
                            // Progress fill
                            RoundedRectangle(cornerRadius: 10)
                                .fill(Color.blue)
                                .frame(width: geometry.size.width * progress, height: 8)
                                .animation(.linear(duration: 0.3), value: progress)
                        }
                    }
                    .frame(height: 8)
                    .padding(.horizontal, 32)
                }
                .padding(.bottom, 60)
            }
        }
        .onAppear {
            startCarousel()
            startProgressSimulation()
        }
    }
    
    private func startCarousel() {
        Timer.scheduledTimer(withTimeInterval: 5.0, repeats: true) { _ in
            withAnimation(.easeInOut(duration: 0.5)) {
                currentTipIndex = (currentTipIndex + 1) % tips.count
            }
        }
    }
    
    private func startProgressSimulation() {
        // Simulate progress (you'll replace this with actual progress tracking)
        Timer.scheduledTimer(withTimeInterval: 0.1, repeats: true) { timer in
            if progress < 1.0 {
                progress += 0.01
            } else {
                timer.invalidate()
            }
        }
    }
}

struct TipContent {
    let icon: String
    let title: String
    let description: String
}

#Preview {
    LoadingOverlay()
}
