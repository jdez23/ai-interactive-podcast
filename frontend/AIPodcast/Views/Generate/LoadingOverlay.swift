import SwiftUI

struct LoadingOverlay: View {
    var body: some View {
        ZStack {
            Color.black.opacity(0.4)
                .ignoresSafeArea()
            
            VStack(spacing: 20) {
                ProgressView()
                    .progressViewStyle(CircularProgressViewStyle(tint: .white))
                    .scaleEffect(1.5)
                
                Text("Generating...")
                    .font(.headline)
                    .foregroundColor(.white)
            }
            .padding(40)
            .background(Color.black.opacity(0.7))
            .cornerRadius(20)
        }
    }
}

#Preview {
    LoadingOverlay()
}
