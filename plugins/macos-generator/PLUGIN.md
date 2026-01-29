# macOS Generator Plugin

> 生成 macOS 原生代码 (Swift + SwiftUI)

## Plugin Information

| Field | Value |
|-------|-------|
| Name | macos-generator |
| Version | 1.0.0 |
| Platform | macOS |
| Hooks | on_generate |

## AI 友好技术栈

| Category | Choice | Reason |
|----------|--------|--------|
| Language | Swift | 现代语法，AI 数据集大 |
| UI | SwiftUI | 声明式 UI，AI 友好 |
| Architecture | MVVM | 最成熟的架构模式 |
| Network | URLSession | 原生 API，无依赖 |
| Database | SwiftData | Apple 最新数据持久化 |
| Async | async/await | Swift 原生异步 |

## Hook: on_generate

### Instructions for AI Agent:

生成 macOS 原生代码时：

1. **项目结构 (Swift + SwiftUI)**
   ```
   macos/
   ├── MyApp/
   │   ├── MyApp.swift              # App 入口
   │   ├── ContentView.swift
   │   ├── Features/
   │   │   ├── Auth/
   │   │   │   ├── Views/
   │   │   │   │   └── LoginView.swift
   │   │   │   └── ViewModels/
   │   │   │       └── LoginViewModel.swift
   │   │   └── Dashboard/
   │   │       └── ...
   │   ├── Core/
   │   │   ├── Network/
   │   │   │   ├── APIClient.swift
   │   │   │   └── Endpoints.swift
   │   │   ├── Models/
   │   │   │   └── User.swift
   │   │   └── Services/
   │   │       └── AuthService.swift
   │   ├── Shared/
   │   │   ├── Components/
   │   │   └── Extensions/
   │   └── Resources/
   │       ├── Assets.xcassets
   │       └── Localizable.strings
   ├── MyApp.xcodeproj
   └── README.md
   ```

2. **代码示例**

   **App 入口**:
   ```swift
   // MyApp.swift
   import SwiftUI
   import SwiftData

   @main
   struct MyApp: App {
       var body: some Scene {
           WindowGroup {
               ContentView()
           }
           .modelContainer(for: [User.self])
       }
   }
   ```

   **数据模型 (SwiftData)**:
   ```swift
   // Core/Models/User.swift
   import Foundation
   import SwiftData

   @Model
   final class User {
       var id: String
       var username: String
       var avatar: String?
       var createdAt: Date

       init(id: String, username: String, avatar: String? = nil) {
           self.id = id
           self.username = username
           self.avatar = avatar
           self.createdAt = Date()
       }
   }
   ```

   **API 客户端**:
   ```swift
   // Core/Network/APIClient.swift
   import Foundation

   actor APIClient {
       static let shared = APIClient()
       
       private let baseURL = URL(string: "https://api.example.com")!
       private var token: String?

       func setToken(_ token: String) {
           self.token = token
       }

       func request<T: Decodable>(
           endpoint: String,
           method: String = "GET",
           body: Encodable? = nil
       ) async throws -> T {
           var request = URLRequest(url: baseURL.appendingPathComponent(endpoint))
           request.httpMethod = method
           request.setValue("application/json", forHTTPHeaderField: "Content-Type")

           if let token {
               request.setValue("Bearer \(token)", forHTTPHeaderField: "Authorization")
           }

           if let body {
               request.httpBody = try JSONEncoder().encode(body)
           }

           let (data, response) = try await URLSession.shared.data(for: request)

           guard let httpResponse = response as? HTTPURLResponse,
                 200..<300 ~= httpResponse.statusCode else {
               throw APIError.invalidResponse
           }

           return try JSONDecoder().decode(T.self, from: data)
       }
   }

   enum APIError: Error {
       case invalidResponse
       case decodingError
   }
   ```

   **ViewModel**:
   ```swift
   // Features/Auth/ViewModels/LoginViewModel.swift
   import Foundation

   @MainActor
   final class LoginViewModel: ObservableObject {
       @Published var username = ""
       @Published var password = ""
       @Published var isLoading = false
       @Published var errorMessage: String?

       func login() async {
           isLoading = true
           errorMessage = nil

           do {
               let response: LoginResponse = try await APIClient.shared.request(
                   endpoint: "/api/v1/auth/login",
                   method: "POST",
                   body: LoginRequest(username: username, password: password)
               )
               await APIClient.shared.setToken(response.token)
               // 处理登录成功
           } catch {
               errorMessage = error.localizedDescription
           }

           isLoading = false
       }
   }
   ```

   **SwiftUI View**:
   ```swift
   // Features/Auth/Views/LoginView.swift
   import SwiftUI

   struct LoginView: View {
       @StateObject private var viewModel = LoginViewModel()

       var body: some View {
           VStack(spacing: 20) {
               Text("登录")
                   .font(.largeTitle)
                   .fontWeight(.bold)

               TextField("用户名", text: $viewModel.username)
                   .textFieldStyle(.roundedBorder)

               SecureField("密码", text: $viewModel.password)
                   .textFieldStyle(.roundedBorder)

               if let error = viewModel.errorMessage {
                   Text(error)
                       .foregroundColor(.red)
                       .font(.caption)
               }

               Button("登录") {
                   Task { await viewModel.login() }
               }
               .buttonStyle(.borderedProminent)
               .disabled(viewModel.isLoading)
           }
           .padding(40)
           .frame(width: 400)
       }
   }
   ```

3. **macOS 特殊考虑**
   - 支持 Menu Bar 和 Dock
   - 处理多窗口
   - 键盘快捷键支持
   - 深色模式自动适配
   - Sandbox 权限配置

## Configuration

```yaml
tech_stack:
  macos:
    language: swift
    min_macos: "13.0"
    ui: swiftui
    architecture: mvvm
    network: urlsession
    database: swiftdata
```
