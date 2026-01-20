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
                        .foregroundColor(.appOrange)
                }
            }
            
            Section("Recent Documents") {
                ForEach(placeholderDocuments, id: \.self) { document in
                    HStack {
                        Image(systemName: "doc.text")
                            .foregroundColor(.appOrange)
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
