import SwiftUI

struct HomeTabView: View {
    @StateObject private var appState = AppState.shared
    
    var body: some View {
        if #available(iOS 16.0, *) {
            NavigationStack {
                VStack(spacing: 0) {
                    // Custom title header
                    HStack(spacing: 10) {
                        Image(systemName: "waveform.circle.fill")
                            .font(.system(size: 28))
                            .foregroundColor(.blue)
                        
                        Text("PROJ430")
                            .font(.largeTitle)
                            .fontWeight(.bold)
                            .foregroundColor(.white)
                        
                        Spacer()
                    }
                    .padding(.horizontal, 20)
                    .padding(.top, 60)
                    .padding(.bottom, 8)
                    .background(Color.black)
                    
                    Group {
                        if appState.generatedPodcasts.isEmpty && appState.downloadedPodcasts.isEmpty {
                            UnpopulatedHomeView()
                        } else {
                            PopulatedHomeView()
                        }
                    }
                }
                .navigationBarHidden(true)
                .background(Color.black.ignoresSafeArea())
            }
        } else {
            NavigationView {
                Group {
                    if appState.generatedPodcasts.isEmpty && appState.downloadedPodcasts.isEmpty {
                        UnpopulatedHomeView()
                    } else {
                        PopulatedHomeView()
                    }
                }
                .navigationTitle("PROJ430")
            }
        }
    }
}

#Preview {
    HomeTabView()
}
