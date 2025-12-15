import SwiftUI

struct UnpopulatedHomeView: View {
    @StateObject private var appState = AppState.shared
    
    var body: some View {
        VStack(spacing: 30) {
            Spacer()
            
            // Logo and Title
            HStack(spacing: 15) {
                Image(systemName: "waveform.circle.fill")
                    .font(.system(size: 60))
                    .foregroundColor(.blue)
                
                Text("PROJ430")
                    .font(.system(size: 40, weight: .bold))
            }
            
            // Description
            Text("Generate your podcast, your way.")
                .font(.title3)
                .multilineTextAlignment(.center)
                .foregroundColor(.secondary)
                .padding(.horizontal, 40)
            
            // CTA Button
            Button(action: {
                appState.switchToGenerate()
            }) {
                HStack {
                    Image(systemName: "plus.circle.fill")
                    Text("Tap to Generate")
                }
                .font(.headline)
                .foregroundColor(.white)
                .frame(maxWidth: .infinity)
                .padding()
                .background(Color.blue)
                .cornerRadius(12)
            }
            .padding(.horizontal, 40)
            .padding(.top, 20)
            
            Spacer()
        }
    }
}

#Preview {
    UnpopulatedHomeView()
}
