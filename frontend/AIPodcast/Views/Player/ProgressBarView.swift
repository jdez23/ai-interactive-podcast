import SwiftUI

struct ProgressBarView: View {
    let currentTime: TimeInterval
    let duration: TimeInterval
    
    var body: some View {
        VStack(spacing: 8) {
            // Progress Bar
            GeometryReader { geometry in
                ZStack(alignment: .leading) {
                    // Background
                    RoundedRectangle(cornerRadius: 2)
                        .fill(Color.gray.opacity(0.3))
                        .frame(height: 4)
                    
                    // Progress
                    RoundedRectangle(cornerRadius: 2)
                        .fill(Color.appOrange)
                        .frame(width: progressWidth(geometry: geometry), height: 4)
                }
            }
            .frame(height: 4)
            
            // Time Labels
            HStack {
                Text(timeString(currentTime))
                    .font(.caption2)
                    .foregroundColor(.secondary)
                
                Spacer()
                
                Text(timeString(duration))
                    .font(.caption2)
                    .foregroundColor(.secondary)
            }
        }
    }
    
    private func progressWidth(geometry: GeometryProxy) -> CGFloat {
        guard duration > 0 else { return 0 }
        let progress = currentTime / duration
        return geometry.size.width * CGFloat(progress)
    }
    
    private func timeString(_ time: TimeInterval) -> String {
        let minutes = Int(time) / 60
        let seconds = Int(time) % 60
        return String(format: "%d:%02d", minutes, seconds)
    }
}

#Preview {
    ProgressBarView(currentTime: 45, duration: 180)
        .padding()
}
