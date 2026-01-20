import SwiftUI

struct AnswerDisplayView: View {
    let question: String
    let answer: QuestionResponse
    let isPlayingAnswer: Bool
    let onDismiss: () -> Void
    let onResume: () -> Void
    
    var body: some View {
        VStack(spacing: 0) {
            // Header
            HStack {
                Image(systemName: "sparkles")
                    .font(.appTitle3)
                    .foregroundColor(.white)
                
                Text("AI Answer")
                    .font(.appTitle3)
                    .foregroundColor(.white)
                
                Spacer()
                
                Button(action: onDismiss) {
                    Image(systemName: "xmark.circle.fill")
                        .font(.title2)
                        .foregroundColor(.white.opacity(0.7))
                }
            }
            .padding(Spacing.md)
            .background(
                LinearGradient(
                    colors: [Color.appPrimary, Color.appAccent],
                    startPoint: .leading,
                    endPoint: .trailing
                )
            )
            
            // Content
            ScrollView {
                VStack(alignment: .leading, spacing: Spacing.lg) {
                    // Question
                    VStack(alignment: .leading, spacing: Spacing.sm) {
                        HStack(spacing: Spacing.xs) {
                            Image(systemName: "questionmark.circle.fill")
                                .font(.appCaption)
                                .foregroundColor(.appPrimary)
                            Text("Your Question")
                                .font(.appCaption)
                                .fontWeight(.semibold)
                                .foregroundColor(.appSecondaryText)
                                .textCase(.uppercase)
                        }
                        
                        Text(question)
                            .font(.appCallout)
                            .foregroundColor(.appText)
                            .padding(Spacing.md)
                            .frame(maxWidth: .infinity, alignment: .leading)
                            .background(Color.appSecondaryBackground)
                            .cornerRadius(CornerRadius.md)
                    }
                    
                    // Audio Playing Indicator
                    if isPlayingAnswer {
                        HStack(spacing: Spacing.sm) {
                            Image(systemName: "waveform")
                                .font(.appCallout)
                                .foregroundColor(.appPrimary)
                                .symbolEffect(.variableColor.iterative.reversing)
                            Text("Playing audio response...")
                                .font(.appCallout)
                                .foregroundColor(.appPrimary)
                        }
                        .padding(Spacing.md)
                        .frame(maxWidth: .infinity)
                        .background(Color.appPrimary.opacity(0.1))
                        .cornerRadius(CornerRadius.md)
                    }
                    
                    // Answer
                    VStack(alignment: .leading, spacing: Spacing.sm) {
                        HStack(spacing: Spacing.xs) {
                            Image(systemName: "lightbulb.fill")
                                .font(.appCaption)
                                .foregroundColor(.appPrimary)
                            Text("Answer")
                                .font(.appCaption)
                                .fontWeight(.semibold)
                                .foregroundColor(.appSecondaryText)
                                .textCase(.uppercase)
                        }
                        
                        Text(answer.answerText)
                            .font(.appBody)
                            .foregroundColor(.appText)
                            .fixedSize(horizontal: false, vertical: true)
                    }
                    
                    // Sources
                    if !answer.sources.isEmpty {
                        VStack(alignment: .leading, spacing: Spacing.sm) {
                            HStack(spacing: Spacing.xs) {
                                Image(systemName: "doc.text.fill")
                                    .font(.appCaption)
                                    .foregroundColor(.appPrimary)
                                Text("Sources")
                                    .font(.appCaption)
                                    .fontWeight(.semibold)
                                    .foregroundColor(.appSecondaryText)
                                    .textCase(.uppercase)
                            }
                            
                            VStack(spacing: Spacing.xs) {
                                ForEach(answer.sources, id: \.self) { source in
                                    HStack(spacing: Spacing.sm) {
                                        Image(systemName: "doc.fill")
                                            .font(.appCaption)
                                            .foregroundColor(.appPrimary)
                                        Text(source)
                                            .font(.appFootnote)
                                            .foregroundColor(.appSecondaryText)
                                        Spacer()
                                    }
                                    .padding(.horizontal, Spacing.md)
                                    .padding(.vertical, Spacing.sm)
                                    .background(Color.appSecondaryBackground)
                                    .cornerRadius(CornerRadius.sm)
                                }
                            }
                        }
                    }
                    
                    // Context Info
                    HStack(spacing: Spacing.lg) {
                        HStack(spacing: Spacing.xs) {
                            Image(systemName: "doc.text")
                                .font(.appCaption)
                                .foregroundColor(.appTertiaryText)
                            Text("\(answer.contextUsed.documentChunks) chunks")
                                .font(.appCaption)
                                .foregroundColor(.appTertiaryText)
                        }
                        
                        HStack(spacing: Spacing.xs) {
                            Image(systemName: "bubble.left.and.bubble.right")
                                .font(.appCaption)
                                .foregroundColor(.appTertiaryText)
                            Text("\(answer.contextUsed.dialogueExchanges) exchanges")
                                .font(.appCaption)
                                .foregroundColor(.appTertiaryText)
                        }
                    }
                    .frame(maxWidth: .infinity)
                }
                .padding(Spacing.md)
            }
            
            // Resume Button
            Button(action: onResume) {
                HStack(spacing: Spacing.sm) {
                    Image(systemName: "play.fill")
                        .font(.appCallout)
                    Text("Resume Podcast")
                        .font(.appCallout)
                        .fontWeight(.semibold)
                }
                .foregroundColor(.white)
                .frame(maxWidth: .infinity)
                .padding(Spacing.md)
                .background(
                    LinearGradient(
                        colors: [Color.appPrimary, Color.appAccent],
                        startPoint: .leading,
                        endPoint: .trailing
                    )
                )
                .cornerRadius(CornerRadius.md)
            }
            .padding(Spacing.md)
        }
        .background(Color.appBackground)
        .cornerRadius(CornerRadius.lg)
        .appCardShadow()
    }
}

#Preview {
    ZStack {
        Color.black.ignoresSafeArea()
        
        AnswerDisplayView(
            question: "What is backpropagation?",
            answer: QuestionResponse(
                answerText: "Backpropagation is an algorithm used to train neural networks by calculating gradients and updating weights based on the error between predicted and actual outputs. It works by propagating the error backwards through the network layers.",
                answerOnly: nil,
                audioUrl: nil,
                sources: ["machine_learning.pdf", "neural_networks.pdf"],
                contextUsed: QuestionResponse.ContextUsed(
                    documentChunks: 5,
                    dialogueExchanges: 3
                ),
                timestamp: 165.5
            ),
            isPlayingAnswer: false,
            onDismiss: {},
            onResume: {}
        )
        .padding(Spacing.md)
    }
}