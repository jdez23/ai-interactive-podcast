import SwiftUI

struct CustomNavBar: View {
    let podcast: Podcast
    let onDismiss: () -> Void
    let onRewind: () -> Void
    
    var body: some View {
        HStack(spacing: 12) {
            // Back Button
            Button(action: onDismiss) {
                Image(systemName: "chevron.down")
                    .font(.title3)
                    .foregroundColor(.primary)
            }
            
            // Thumbnail
            RoundedRectangle(cornerRadius: 6)
                .fill(Color.gray.opacity(0.3))
                .frame(width: 40, height: 40)
                .overlay(
                    Image(systemName: "waveform")
                        .font(.caption)
                        .foregroundColor(.white)
                )
            
            // Title & Subtitle
            VStack(alignment: .leading, spacing: 2) {
                Text("Episode")
                    .font(.caption)
                    .fontWeight(.semibold)
                    .lineLimit(1)
                
                Text("Generated Podcast")
                    .font(.caption2)
                    .foregroundColor(.secondary)
                    .lineLimit(1)
            }
            
            Spacer()
            
            // Controls
            HStack(spacing: 15) {
                Button(action: onRewind) {
                    Image(systemName: "gobackward.10")
                        .font(.title3)
                }
                
                // Play button handled in main controls
            }
            .foregroundColor(.primary)
        }
        .padding()
        .background(.background)
        .shadow(color: .black.opacity(0.1), radius: 2, y: 2)
    }
}

