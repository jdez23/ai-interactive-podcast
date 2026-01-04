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
                }
                Text("Generate")
            }
        }
        .buttonStyle(PrimaryButtonStyle(isEnabled: !isGenerating))
        .disabled(isGenerating)
    }
}

#Preview {
    ZStack {
        Color.black.ignoresSafeArea()
        
        VStack(spacing: 20) {
            GenerateButton(isGenerating: false, onGenerate: {})
            GenerateButton(isGenerating: true, onGenerate: {})
        }
        .padding()
    }
}

