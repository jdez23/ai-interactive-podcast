import SwiftUI

struct AddFileEmptyState: View {
    let onAddFile: () -> Void
    
    var body: some View {
        Button(action: onAddFile) {
            VStack(spacing: 16) {
                VStack(spacing: 12) {
                    // Blue circle with plus icon
                    ZStack {
                        Circle()
                            .fill(Color.appPrimary)
                            .frame(width: 56, height: 56)
                        
                        Image(systemName: "plus")
                            .font(.system(size: 24, weight: .medium))
                            .foregroundColor(.white)
                    }
                    
                    Text("Add file")
                        .font(.title3)
                        .fontWeight(.semibold)
                        .foregroundColor(.white)
                    
                    Text("Add file(s) to generate your personalized\npodcast")
                        .font(.subheadline)
                        .foregroundColor(.gray)
                        .multilineTextAlignment(.center)
                }
            }
            .frame(maxWidth: .infinity, maxHeight: .infinity)
            .contentShape(Rectangle())
        }
        .buttonStyle(.plain)
    }
}

#Preview {
    ZStack {
        Color.black.ignoresSafeArea()
        AddFileEmptyState(onAddFile: {})
    }
}
