import SwiftUI

struct AddFileBox: View {
    let onAddFile: () -> Void
    
    var body: some View {
        Button(action: onAddFile) {
            VStack(spacing: 12) {
                // Blue circle with plus icon
                ZStack {
                    Circle()
                        .fill(Color.appPrimary)
                        .frame(width: 48, height: 48)
                    
                    Image(systemName: "plus")
                        .font(.system(size: 20, weight: .medium))
                        .foregroundColor(.white)
                }
                
                Text("Add file")
                    .font(.headline)
                    .foregroundColor(.white)
                
                Text("Add files to generate your personalized\npodcast")
                    .font(.caption)
                    .foregroundColor(.gray)
                    .multilineTextAlignment(.center)
            }
            .frame(maxWidth: .infinity)
            .padding(.vertical, 24)
            .background(
                RoundedRectangle(cornerRadius: 12)
                    .strokeBorder(Color.gray.opacity(0.3), lineWidth: 1)
            )
            .contentShape(Rectangle())
        }
        .buttonStyle(.plain)
    }
}

#Preview {
    ZStack {
        Color.black.ignoresSafeArea()
        AddFileBox(onAddFile: {})
            .padding()
    }
}
