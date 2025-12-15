import SwiftUI

struct AddFileSection: View {
    let hasFiles: Bool
    let onAddFile: () -> Void
    
    var body: some View {
        Button(action: onAddFile) {
            HStack {
                Image(systemName: "plus.circle.fill")
                    .font(.system(size: hasFiles ? 24 : 30))
                    .foregroundColor(.blue)
                
                VStack(alignment: .leading, spacing: 4) {
                    Text("Add file")
                        .font(hasFiles ? .headline : .title3)
                        .fontWeight(.semibold)
                    
                    Text("Add file(s) to generate your personalized podcast")
                        .font(.caption)
                        .foregroundColor(.secondary)
                }
                Spacer()
            }
            .padding()
            .background(Color.gray.opacity(0.1))
            .cornerRadius(12)
        }
        .buttonStyle(PlainButtonStyle())
    }
}

#Preview {
    VStack {
        AddFileSection(hasFiles: false, onAddFile: {})
        AddFileSection(hasFiles: true, onAddFile: {})
    }
    .padding()
}
