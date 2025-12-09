import SwiftUI

struct DocumentTabView: View {
    var body: some View {
        NavigationStack {
            DocumentListView()
                .navigationTitle("Documents")
        }
    }
}

#Preview {
    DocumentTabView()
}
