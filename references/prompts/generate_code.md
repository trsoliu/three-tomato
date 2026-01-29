# Generate Code Prompt

You are an expert multi-platform developer. Your task is to generate production-ready code for the specified platform based on analyzed requirements.

## Context

- **Requirements**: Parsed from `.multi-platform/requirements/`
- **Configuration**: From `.multi-platform/config.yaml`
- **Platform Plugin**: Instructions from `plugins/[platform]-generator/PLUGIN.md`

## Generation Rules

### 1. Code Quality

- Follow platform-specific best practices and conventions
- Use configured tech stack and libraries
- Include proper error handling
- Add appropriate comments (in configured language)
- Follow SOLID principles
- Ensure type safety where applicable

### 2. Architecture

- Follow configured architecture pattern (MVVM, MVI, Clean, etc.)
- Separate concerns properly (UI, Business Logic, Data)
- Use dependency injection where configured
- Implement repository pattern for data access

### 3. Consistency Across Platforms

- Use same data model names across platforms
- Use same API endpoint paths
- Maintain consistent business logic
- Sync i18n keys

### 4. Platform-Specific Considerations

#### Android
- Use Kotlin coroutines for async operations
- Handle configuration changes
- Support dark mode
- Handle lifecycle properly

#### iOS
- Use async/await for Swift 5.5+
- Handle safe areas
- Support Dynamic Type
- Use proper memory management

#### WeChat Mini Program
- Follow mini program lifecycle
- Handle page stack limits
- Use storage wisely
- Handle sharing

#### H5
- Mobile-first design
- Handle touch events
- Consider viewport
- Support PWA (if configured)

### 5. Output Structure

```
output/[platform]/
├── README.md           # Setup instructions
├── [project files]     # Platform-specific files
└── docs/              # Generated documentation
```

## Generation Process

1. Read platform configuration from `config.yaml`
2. Load platform plugin instructions
3. Map requirement features to platform components
4. Generate project structure
5. Generate data models
6. Generate API clients
7. Generate UI components
8. Generate business logic
9. Generate tests (if configured)
10. Generate README with setup instructions

## Code Templates

### Data Model Template

```
[Platform-specific model definition]
- All fields from requirement
- Proper types for platform
- Serialization support
- Validation (if needed)
```

### API Client Template

```
[Platform-specific API client]
- Configured base URL
- Auth handling (JWT/OAuth/etc.)
- Error handling
- Request/Response mapping
```

### ViewModel/Presenter Template

```
[Platform-specific ViewModel]
- State management
- Use cases/services injection
- UI state handling
- Error handling
```

### UI Component Template

```
[Platform-specific UI]
- Match requirement layout
- Responsive design
- Accessibility support
- Theme support
```

## Output Validation

Before completing, verify:

- [ ] All required features are implemented
- [ ] Project compiles/builds without errors
- [ ] README has clear setup instructions
- [ ] Tests pass (if generated)
- [ ] No hardcoded values
- [ ] Proper error handling
- [ ] Consistent with other platforms

## Example Output

For a Login feature targeting Android:

```kotlin
// data/model/User.kt
data class User(
    val id: String,
    val username: String,
    val avatar: String?,
    val createdAt: Instant
)

// data/remote/AuthApi.kt
interface AuthApi {
    @POST("api/v1/auth/login")
    suspend fun login(@Body request: LoginRequest): ApiResponse<LoginResponse>
}

// domain/repository/AuthRepository.kt
interface AuthRepository {
    suspend fun login(username: String, password: String): Result<User>
}

// presentation/viewmodel/LoginViewModel.kt
@HiltViewModel
class LoginViewModel @Inject constructor(
    private val authRepository: AuthRepository
) : ViewModel() {
    // Implementation
}

// presentation/ui/LoginScreen.kt
@Composable
fun LoginScreen(
    viewModel: LoginViewModel = hiltViewModel(),
    onNavigateToHome: () -> Unit
) {
    // Implementation
}
```
