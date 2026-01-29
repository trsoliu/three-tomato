# iOS Generator Plugin

> Generate native iOS code from requirement documents.

## Plugin Information

| Field | Value |
|-------|-------|
| Name | ios-generator |
| Version | 1.0.0 |
| Platform | iOS |
| Hooks | on_generate |

## Supported Tech Stacks

| Category | Options | Default |
|----------|---------|---------|
| Language | Swift, Objective-C | Swift |
| Architecture | MVVM, VIPER, Clean, TCA | MVVM |
| UI | SwiftUI, UIKit, Hybrid | SwiftUI |
| Network | Alamofire, URLSession, Moya, gRPC-Swift | Alamofire |
| Image | Kingfisher, SDWebImage, Nuke | Kingfisher |
| Database | Core Data, Realm, GRDB | Core Data |
| Async | Combine, RxSwift, async/await | Combine |
| Package | SPM, CocoaPods, Carthage | SPM |

## Hook: on_generate

### Instructions for AI Agent:

When generating iOS code:

1. **Read Configuration**
   - Check `tech_stack.ios` in config.yaml
   - Apply language, architecture, and library choices

2. **Project Structure (Swift + MVVM + SwiftUI)**
   ```
   ios/
   ├── App/
   │   ├── Sources/
   │   │   ├── App/
   │   │   │   ├── AppDelegate.swift
   │   │   │   └── MyApp.swift
   │   │   ├── Features/
   │   │   │   ├── Auth/
   │   │   │   │   ├── Views/
   │   │   │   │   │   └── LoginView.swift
   │   │   │   │   ├── ViewModels/
   │   │   │   │   │   └── LoginViewModel.swift
   │   │   │   │   └── Models/
   │   │   │   │       └── LoginRequest.swift
   │   │   │   └── Home/
   │   │   │       └── ...
   │   │   ├── Core/
   │   │   │   ├── Network/
   │   │   │   │   ├── APIClient.swift
   │   │   │   │   ├── APIEndpoint.swift
   │   │   │   │   └── NetworkError.swift
   │   │   │   ├── Storage/
   │   │   │   │   └── UserDefaults+Extension.swift
   │   │   │   └── Utils/
   │   │   │       └── Extensions/
   │   │   ├── Models/
   │   │   │   ├── User.swift
   │   │   │   └── APIResponse.swift
   │   │   ├── Services/
   │   │   │   ├── AuthService.swift
   │   │   │   └── UserService.swift
   │   │   └── Resources/
   │   │       ├── Assets.xcassets/
   │   │       └── Localizable.strings
   │   ├── Tests/
   │   │   └── ...
   │   └── Package.swift
   ├── .gitignore
   └── README.md
   ```

3. **Code Generation Rules**

   **Data Models** - Convert from requirement:
   ```swift
   // From requirement: User entity
   struct User: Codable, Identifiable {
       let id: String
       let username: String
       let avatar: String?
       let createdAt: Date
   }
   ```

   **API Client**:
   
   *Option A: HTTP/REST (Default)*
   ```swift
   protocol APIClientProtocol {
       func request<T: Decodable>(_ endpoint: APIEndpoint) async throws -> T
   }
   // ... implementation
   ```

   *Option B: gRPC (If specified or legacy used gRPC)*
   ```swift
   import GRPC
   import NIO
   
   final class GRPCClient {
       private let channel: ClientConnection
       
       init(host: String, port: Int) {
           let group = MultiThreadedEventLoopGroup(numberOfThreads: 1)
           self.channel = ClientConnection.insecure(group: group)
               .connect(host: host, port: port)
       }
       
       // Expose services
       lazy var artistService = ArtistService_ServiceClient(channel: channel)
   }
   ```

   **Service Layer**:
   ```swift
   protocol AuthServiceProtocol {
       func login(username: String, password: String) async throws -> User
   }
   
   final class AuthService: AuthServiceProtocol {
       private let apiClient: APIClientProtocol
       
       func login(username: String, password: String) async throws -> User {
           // Implementation
       }
   }
   ```

   **ViewModel**:
   ```swift
   @MainActor
   final class LoginViewModel: ObservableObject {
       @Published var username = ""
       @Published var password = ""
       @Published var isLoading = false
       @Published var error: Error?
       
       private let authService: AuthServiceProtocol
       
       func login() async {
           isLoading = true
           defer { isLoading = false }
           
           do {
               let user = try await authService.login(
                   username: username,
                   password: password
               )
               // Handle success
           } catch {
               self.error = error
           }
       }
   }
   ```

   **SwiftUI View**:
   ```swift
   struct LoginView: View {
       @StateObject private var viewModel = LoginViewModel()
       
       var body: some View {
           VStack(spacing: 20) {
               TextField("Username", text: $viewModel.username)
                   .textFieldStyle(.roundedBorder)
               
               SecureField("Password", text: $viewModel.password)
                   .textFieldStyle(.roundedBorder)
               
               Button("Login") {
                   Task { await viewModel.login() }
               }
               .buttonStyle(.borderedProminent)
               .disabled(viewModel.isLoading)
           }
           .padding()
       }
   }
   ```

4. **Platform-Specific Considerations**
   - Support dark mode via `@Environment(\.colorScheme)`
   - Handle safe area insets
   - Support Dynamic Type for accessibility
   - Handle iPhone and iPad layouts
   - Consider notch and home indicator areas

5. **Dependencies** - Add to Package.swift:
   ```swift
   dependencies: [
       .package(url: "https://github.com/Alamofire/Alamofire.git", from: "5.8.0"),
       .package(url: "https://github.com/onevcat/Kingfisher.git", from: "7.10.0"),
   ]
   ```

## Output Files

| File | Description |
|------|-------------|
| `Package.swift` | SPM manifest |
| `Sources/App/` | Application entry |
| `Sources/Features/` | Feature modules |
| `Sources/Core/` | Core utilities |
| `Sources/Models/` | Data models |
| `Sources/Services/` | Service layer |
| `Tests/` | Unit tests |
| `README.md` | Setup instructions |

## Configuration

```yaml
tech_stack:
  ios:
    language: swift
    min_ios: "15.0"
    architecture: mvvm
    ui: swiftui
    network: alamofire
    image: kingfisher
    database: coredata
    async: combine
    package_manager: spm
```
