import SwiftUI

struct AskAISection: View {
    @Binding var question: String
    let isProcessing: Bool
    let onTapToAsk: () -> Void
    let onSubmitText: () -> Void
    
    var body: some View {
        VStack(spacing: 15) {
            // Tap to Ask (Voice)
            Button(action: onTapToAsk) {
                HStack {
                    Image(systemName: "mic.fill")
                        .font(.title2)
                    Text("Tap to ask AI")
                        .font(.headline)
                }
                .foregroundColor(.white)
                .frame(maxWidth: .infinity)
                .padding()
                .background(Color.blue)
                .cornerRadius(12)
            }
            .disabled(isProcessing)
            
            // Type to Ask
            HStack {
                TextField("Type to ask AI...", text: $question)
                    .textFieldStyle(RoundedBorderTextFieldStyle())
                    .disabled(isProcessing)
                
                Button(action: onSubmitText) {
                    if isProcessing {
                        ProgressView()
                    } else {
                        Image(systemName: "paperplane.fill")
                            .foregroundColor(.blue)
                    }
            }
            .disabled(question.isEmpty || isProcessing)
        }
    }
}

}
#Preview {
AskAISection(
question: .constant(""),
isProcessing: false,
onTapToAsk: {},
onSubmitText: {}
)
.padding()
}
