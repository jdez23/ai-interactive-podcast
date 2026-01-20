import SwiftUI

struct LoadingView: View {
    let message: String
    let showBackground: Bool
    
    init(message: String = "Loading...", showBackground: Bool = true) {
        self.message = message
        self.showBackground = showBackground
    }
    
    var body: some View {
        VStack(spacing: Spacing.md) {
            ProgressView()
                .progressViewStyle(CircularProgressViewStyle(tint: .appPrimary))
                .scaleEffect(1.5)
            
            Text(message)
                .font(.appCallout)
                .foregroundColor(.appSecondaryText)
        }
        .padding(Spacing.xl)
        .background(
            showBackground ? Color.appCardBackground : Color.clear
        )
        .cornerRadius(CornerRadius.lg)
        .appLightShadow()
    }
}

// MARK: - Full Screen Loading Overlay
struct LoadingOverlayView: View {
    let message: String
    
    init(message: String = "Loading...") {
        self.message = message
    }
    
    var body: some View {
        ZStack {
            Color.black.opacity(0.4)
                .ignoresSafeArea()
            
            VStack(spacing: Spacing.lg) {
                ProgressView()
                    .progressViewStyle(CircularProgressViewStyle(tint: .white))
                    .scaleEffect(2)
                
                Text(message)
                    .font(.appBodyBold)
                    .foregroundColor(.white)
            }
            .padding(Spacing.xxl)
            .background(Color.black.opacity(0.8))
            .cornerRadius(CornerRadius.xl)
        }
    }
}

// MARK: - Inline Loading (for small spaces)
struct InlineLoadingView: View {
    let message: String?
    
    init(message: String? = nil) {
        self.message = message
    }
    
    var body: some View {
        HStack(spacing: Spacing.sm) {
            ProgressView()
                .progressViewStyle(CircularProgressViewStyle(tint: .appSecondaryText))
                .scaleEffect(0.8)
            
            if let message = message {
                Text(message)
                    .font(.appFootnote)
                    .foregroundColor(.appSecondaryText)
            }
        }
    }
}

// MARK: - Skeleton Loading (placeholder animation)
struct SkeletonLoadingView: View {
    @State private var isAnimating = false
    
    let height: CGFloat
    let cornerRadius: CGFloat
    
    init(height: CGFloat = 20, cornerRadius: CGFloat = CornerRadius.sm) {
        self.height = height
        self.cornerRadius = cornerRadius
    }
    
    var body: some View {
        RoundedRectangle(cornerRadius: cornerRadius)
            .fill(Color.appTertiaryBackground)
            .frame(height: height)
            .overlay(
                RoundedRectangle(cornerRadius: cornerRadius)
                    .fill(
                        LinearGradient(
                            colors: [
                                Color.clear,
                                Color.white.opacity(0.3),
                                Color.clear
                            ],
                            startPoint: .leading,
                            endPoint: .trailing
                        )
                    )
                    .offset(x: isAnimating ? 200 : -200)
            )
            .clipped()
            .onAppear {
                withAnimation(
                    Animation.linear(duration: 1.5)
                        .repeatForever(autoreverses: false)
                ) {
                    isAnimating = true
                }
            }
    }
}

// MARK: - Previews
#Preview("Loading Views - Light Mode") {
    VStack(spacing: Spacing.xl) {
        Text("Standard Loading View")
            .font(.appTitle3)
        LoadingView(message: "Generating...")
        
        Text("Without Background")
            .font(.appTitle3)
        LoadingView(message: "Generating...", showBackground: false)
        
        Text("Inline Loading")
            .font(.appTitle3)
        InlineLoadingView(message: "Generating...")
        
        Text("Skeleton Loading")
            .font(.appTitle3)
        VStack(spacing: Spacing.sm) {
            SkeletonLoadingView(height: 60)
            SkeletonLoadingView(height: 40)
            SkeletonLoadingView(height: 40)
        }
        .padding(.horizontal)
    }
    .padding()
}

#Preview("Loading Overlay") {
    ZStack {
        // Simulated content behind overlay
        VStack {
            Text("Main Content")
            Button("Button") {}
        }
        
        LoadingOverlayView(message: "Generating podcast...")
    }
}

#Preview("Loading Views - Dark Mode") {
    VStack(spacing: Spacing.xl) {
        LoadingView(message: "Loading your data...")
        
        InlineLoadingView(message: "Processing...")
        
        VStack(spacing: Spacing.sm) {
            SkeletonLoadingView(height: 60)
            SkeletonLoadingView(height: 40)
        }
        .padding(.horizontal)
    }
    .padding()
    .preferredColorScheme(.light)
}
