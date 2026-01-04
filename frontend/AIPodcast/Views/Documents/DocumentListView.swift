import SwiftUI

struct DocumentListView: View {
    // Placeholder data
    let placeholderDocuments = [
        "Java.pdf",
        "Onboarding.pdf",
        "Python.pdf"
    ]
    
    var body: some View {
        List {
            Section {
                NavigationLink {
                    GenerateTabView()
                } label: {
                    Label("Upload PDFs to Generate", systemImage: "arrow.up.doc")
                        .foregroundColor(.blue)
                }
            }
            
            Section("Recent Documents") {
                ForEach(placeholderDocuments, id: \.self) { document in
                    HStack {
                        Image(systemName: "doc.text")
                            .foregroundColor(.blue)
                        Text(document)
                    }
                }
            }
        }
    }
}

#Preview {
    DocumentListView()
}
