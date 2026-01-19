import SwiftUI

struct PlaybackControlsView: View {
    let isPlaying: Bool
    let onPlayPause: () -> Void
    
    var body: some View {
        HStack(spacing: 40) {
            Spacer()
            
            // Play/Pause Button
            Button(action: onPlayPause) {
                Image(systemName: isPlaying ? "pause.circle.fill" : "play.circle.fill")
                    .font(.system(size: 70))
                    .foregroundColor(.appOrange)
            }
            
            Spacer()
        }
    }
}

#Preview {
    VStack {
        PlaybackControlsView(isPlaying: false, onPlayPause: {})
        PlaybackControlsView(isPlaying: true, onPlayPause: {})
    }
}
