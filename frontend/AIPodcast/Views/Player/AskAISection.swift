import SwiftUI

struct AskAISection: View {
    @Binding var question: String
    let isProcessing: Bool
    let onSubmitText: () -> Void
    @FocusState private var isTextFieldFocused: Bool
    
    var body: some View {
        VStack(spacing: 15) {
            // Tap to Ask (Voice) - COMMENTED OUT FOR NOW
            /*
            Button(action: onTapToAsk) {
                HStack {
                    if isWaitingForHost {
                        ProgressView()
                            .progressViewStyle(CircularProgressViewStyle(tint: .white))
                        Text("Waiting for host...")
                            .font(.headline)
                    } else {
                        Image(systemName: isRecording ? "stop.circle.fill" : "mic.fill")
                            .font(.title2)
                            .symbolEffect(.pulse, isActive: isRecording)
                        Text(isRecording ? "Tap to stop recording" : "Tap to ask AI")
                            .font(.headline)
                    }
                }
                .foregroundColor(.white)
                .frame(maxWidth: .infinity)
                .padding()
                .background(isWaitingForHost ? Color.orange : (isRecording ? Color.red : Color.blue))
                .cornerRadius(12)
            }
            .disabled(isProcessing || isWaitingForHost)
            
            Text("or")
                .font(.caption)
                .foregroundColor(.secondary)
            */
            
            // Type to Ask
            HStack {
                TextField("Type to ask AI...", text: $question)
                    .textFieldStyle(RoundedBorderTextFieldStyle())
                    .disabled(isProcessing)
                    .focused($isTextFieldFocused)
                    .onAppear {
                        DispatchQueue.main.asyncAfter(deadline: .now() + 0.5) {
                            isTextFieldFocused = true
                        }
                    }
                
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
        onSubmitText: {}
    )
    .padding()
}
