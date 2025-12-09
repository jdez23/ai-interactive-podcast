import SwiftUI

struct DocumentListView: View {
    // Placeholder data
    let placeholderDocuments = [
        "American Revolution.pdf",
        "World War II.pdf",
        "Ancient Greece.pdf"
    ]
    
    var body: some View {
        List(placeholderDocuments, id: \.self) { document in
            HStack {
                Image(systemName: "doc.text")
                    .foregroundColor(.blue)
                Text(document)
            }
        }
    }
}

#Preview {
    DocumentListView()
}
