# Android Generator Plugin

> Generate native Android code from requirement documents.

## Plugin Information

| Field | Value |
|-------|-------|
| Name | android-generator |
| Version | 1.0.0 |
| Platform | Android |
| Hooks | on_generate |

## Supported Tech Stacks

| Category | Options | Default |
|----------|---------|---------|
| Language | Kotlin, Java | Kotlin |
| Architecture | MVVM, MVP, MVI, Clean Architecture | MVVM |
| DI | Hilt, Koin, Dagger, Manual | Hilt |
| Network | Retrofit, OkHttp, Ktor | Retrofit |
| Image | Coil, Glide, Picasso | Coil |
| Database | Room, Realm, SQLDelight | Room |
| Async | Coroutines, RxJava | Coroutines |
| UI | Jetpack Compose, XML, Hybrid | Compose |

## Hook: on_generate

### Instructions for AI Agent:

When generating Android code:

1. **Read Configuration**
   - Check `tech_stack.android` in config.yaml
   - Apply language, architecture, and library choices

2. **Project Structure (Kotlin + MVVM + Compose)**
   ```
   android/
   ├── app/
   │   ├── src/main/
   │   │   ├── java/com/example/app/
   │   │   │   ├── di/                    # Hilt modules
   │   │   │   ├── data/
   │   │   │   │   ├── model/             # Data models
   │   │   │   │   ├── repository/        # Repositories
   │   │   │   │   ├── remote/            # API services
   │   │   │   │   └── local/             # Local database
   │   │   │   ├── domain/
   │   │   │   │   ├── model/             # Domain models
   │   │   │   │   ├── repository/        # Repository interfaces
   │   │   │   │   └── usecase/           # Use cases
   │   │   │   ├── presentation/
   │   │   │   │   ├── ui/
   │   │   │   │   │   ├── theme/         # Compose theme
   │   │   │   │   │   ├── components/    # Reusable components
   │   │   │   │   │   └── screens/       # Screen composables
   │   │   │   │   └── viewmodel/         # ViewModels
   │   │   │   ├── util/                  # Utilities
   │   │   │   └── App.kt                 # Application class
   │   │   ├── res/
   │   │   │   ├── values/
   │   │   │   └── ...
   │   │   └── AndroidManifest.xml
   │   └── build.gradle.kts
   ├── gradle/
   ├── build.gradle.kts
   ├── settings.gradle.kts
   └── README.md
   ```

3. **Code Generation Rules**

   **Data Models** - Convert from requirement:
   ```kotlin
   // From requirement: User entity
   data class User(
       val id: String,
       val username: String,
       val avatar: String?,
       val createdAt: Instant
   )
   ```

   **API Service** - Generate from API specs:
   ```kotlin
   interface ApiService {
       @POST("api/v1/auth/login")
       suspend fun login(@Body request: LoginRequest): Response<LoginResponse>
   }
   ```

   **Repository**:
   ```kotlin
   interface UserRepository {
       suspend fun login(username: String, password: String): Result<User>
   }
   ```

   **ViewModel**:
   ```kotlin
   @HiltViewModel
   class LoginViewModel @Inject constructor(
       private val userRepository: UserRepository
   ) : ViewModel() {
       // StateFlow for UI state
       // Handle user actions
   }
   ```

   **Compose Screen**:
   ```kotlin
   @Composable
   fun LoginScreen(
       viewModel: LoginViewModel = hiltViewModel(),
       onNavigateToHome: () -> Unit
   ) {
       // UI implementation
   }
   ```

4. **Platform-Specific Considerations**
   - Add necessary permissions to AndroidManifest.xml
   - Handle configuration changes
   - Support dark mode via MaterialTheme
   - Handle back navigation properly
   - Consider screen sizes and orientations

5. **Dependencies** - Add to build.gradle.kts:
   ```kotlin
   dependencies {
       // Core
       implementation("androidx.core:core-ktx:1.12.0")
       implementation("androidx.lifecycle:lifecycle-runtime-ktx:2.7.0")
       
       // Compose
       implementation(platform("androidx.compose:compose-bom:2024.01.00"))
       implementation("androidx.compose.ui:ui")
       implementation("androidx.compose.material3:material3")
       
       // Hilt
       implementation("com.google.dagger:hilt-android:2.50")
       kapt("com.google.dagger:hilt-compiler:2.50")
       
       // Retrofit
       implementation("com.squareup.retrofit2:retrofit:2.9.0")
       implementation("com.squareup.retrofit2:converter-gson:2.9.0")
       
       // Room
       implementation("androidx.room:room-runtime:2.6.1")
       implementation("androidx.room:room-ktx:2.6.1")
       kapt("androidx.room:room-compiler:2.6.1")
       
       // Coil
       implementation("io.coil-kt:coil-compose:2.5.0")
   }
   ```

## Output Files

| File | Description |
|------|-------------|
| `build.gradle.kts` | Root build config |
| `app/build.gradle.kts` | App module config |
| `settings.gradle.kts` | Project settings |
| `app/src/main/AndroidManifest.xml` | Manifest |
| `app/src/main/java/.../` | Source code |
| `app/src/main/res/` | Resources |
| `README.md` | Setup instructions |

## Configuration

```yaml
tech_stack:
  android:
    language: kotlin
    min_sdk: 24
    target_sdk: 34
    architecture: mvvm
    di: hilt
    network: retrofit
    image: coil
    database: room
    async: coroutines
    ui: compose
```
