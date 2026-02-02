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

   *Option B: gRPC/Protobuf via JSON Transcoding (推荐)*
   
   **Rules**:
   1. **直接使用生成的类型**：不要在 pb.swift 基础上手写复杂封装层
   2. **Source of Truth**: 使用 `.proto` 文件从遗留项目或指定路径
   3. **Generation Strategy**:
      - Copy `.proto` files to `Core/Network/Proto/Definitions`
      - Create `generate_protos.sh` using `protoc --swift_out`
      - Add `SwiftProtobuf` dependency via SPM
   
   **简洁 APIClient 模式** (避免 IOS-001/002 问题):
   ```swift
   import Foundation
   import SwiftProtobuf
   
   class APIClient {
       static let shared = APIClient()
       private let baseURL = "https://api.quanku.art"
       
       func call<Req: SwiftProtobuf.Message, Res: SwiftProtobuf.Message>(
           service: String, method: String, request: Req
       ) async throws -> Res {
           let url = URL(string: "\(baseURL)/\(service)/\(method)")!
           var urlRequest = URLRequest(url: url)
           urlRequest.httpMethod = "POST"
           urlRequest.setValue("application/json", forHTTPHeaderField: "Content-Type")
           urlRequest.httpBody = try request.jsonUTF8Data()  // SwiftProtobuf 方法
           
           let (data, _) = try await URLSession.shared.data(for: urlRequest)
           return try Res(jsonUTF8Data: data)  // SwiftProtobuf 方法
       }
       
       // 业务方法直接使用生成的类型
       func getArtist(id: String) async throws -> Cag2_Artist {
           var req = Cag2_GetReq()
           req.id = id
           return try await call(service: "cag2.ArtistService", method: "get", request: req)
       }
   }
   ```
   
   **⚠️ 已知问题提醒** (see known-issues.yaml):
   - IOS-001: 不要过度封装，直接用生成类型
   - IOS-002: 用 `jsonUTF8Data()` 而非 `JSONEncoder`
   - IOS-003: 确保 pb.swift 加入 Sources build phase
   - IOS-004: 检查生成代码的实际属性名

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
