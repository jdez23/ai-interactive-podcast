import SwiftUI

struct PodcastListView: View {
    // Placeholder data
    let placeholderPodcasts = [
        "The American Revolution - 5 min",
        "World War II Overview - 10 min",
        "Ancient Greece Culture - 8 min"
    ]
    
    var body: some View {
        List(placeholderPodcasts, id: \.self) { podcast in
            HStack {
                Image(systemName: "waveform.circle.fill")
                    .foregroundColor(.purple)
                    .font(.title2)
                VStack(alignment: .leading) {
                    Text(podcast)
                        .font(.headline)
                }
            }
            .padding(.vertical, 4)
        }
    }
}

#Preview {
    PodcastListView()
}
