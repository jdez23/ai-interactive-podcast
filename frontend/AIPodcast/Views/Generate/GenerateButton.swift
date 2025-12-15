import SwiftUI

struct GenerateButton: View {
    let isGenerating: Bool
    let onGenerate: () -> Void
    
    var body: some View {
        Button(action: onGenerate) {
            HStack {
                if isGenerating {
                    ProgressView()
                        .progressViewStyle(CircularProgressViewStyle(tint: .white))
                    Text("Generating...")
                } else {
                    Image(systemName: "waveform.circle.fill")
                    Text("Generate Podcast")
                }
            }
            .font(.headline)
            .foregroundColor(.white)
            .frame(maxWidth: .infinity)
            .padding()
            .background(isGenerating ? Color.gray : Color.blue)
            .cornerRadius(12)
        }
        .disabled(isGenerating)
    }
}

#Preview {
    VStack {
        GenerateButton(isGenerating: false, onGenerate: {})
        GenerateButton(isGenerating: true, onGenerate: {})
    }
    .padding()
}
