import SwiftUI
import Alamofire

struct TestView: View {
    var body: some View {
        VStack {
            Text("Project Setup Test")
            Text("API URL: \(Constants.apiBaseURL)")
                .font(.caption)
        }
    }
}

struct TestView_Previews: PreviewProvider {
    static var previews: some View {
        TestView()
    }
}
