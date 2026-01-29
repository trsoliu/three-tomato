# Flutter Generator Plugin

> Flutter 跨端代码生成 (Dart + Riverpod)

## Plugin Information

| Field | Value |
|-------|-------|
| Name | flutter-generator |
| Version | 1.0.0 |
| Platform | Flutter (iOS, Android, Web, Desktop) |
| Hooks | on_generate |

## AI 友好技术栈

| Category | Choice | Reason |
|----------|--------|--------|
| Language | Dart | 类型安全，AI 数据集适中 |
| State | Riverpod | 现代状态管理，类型安全 |
| Network | Dio | 功能强大，文档丰富 |
| Router | go_router | 声明式路由 |
| DI | Riverpod | 内置依赖注入 |

## Hook: on_generate

### Instructions for AI Agent:

生成 Flutter 代码时：

1. **项目结构**
   ```
   flutter/
   ├── lib/
   │   ├── main.dart
   │   ├── app.dart
   │   ├── core/
   │   │   ├── constants/
   │   │   ├── extensions/
   │   │   ├── theme/
   │   │   └── utils/
   │   ├── data/
   │   │   ├── models/
   │   │   ├── repositories/
   │   │   └── services/
   │   ├── presentation/
   │   │   ├── pages/
   │   │   ├── widgets/
   │   │   └── providers/
   │   └── router/
   │       └── app_router.dart
   ├── test/
   ├── pubspec.yaml
   └── README.md
   ```

2. **代码示例**

   **数据模型**:
   ```dart
   // lib/data/models/user.dart
   import 'package:freezed_annotation/freezed_annotation.dart';

   part 'user.freezed.dart';
   part 'user.g.dart';

   @freezed
   class User with _$User {
     const factory User({
       required String id,
       required String username,
       String? avatar,
       required DateTime createdAt,
     }) = _User;

     factory User.fromJson(Map<String, dynamic> json) => _$UserFromJson(json);
   }
   ```

   **API Service**:
   ```dart
   // lib/data/services/api_service.dart
   import 'package:dio/dio.dart';
   import 'package:riverpod_annotation/riverpod_annotation.dart';

   part 'api_service.g.dart';

   @riverpod
   Dio dio(DioRef ref) {
     final dio = Dio(BaseOptions(
       baseUrl: 'https://api.example.com',
       connectTimeout: const Duration(seconds: 10),
     ));
     
     dio.interceptors.add(InterceptorsWrapper(
       onRequest: (options, handler) {
         // Add auth token
         handler.next(options);
       },
     ));
     
     return dio;
   }

   @riverpod
   ApiService apiService(ApiServiceRef ref) {
     return ApiService(ref.watch(dioProvider));
   }

   class ApiService {
     final Dio _dio;
     ApiService(this._dio);

     Future<T> get<T>(String path) async {
       final response = await _dio.get(path);
       return response.data;
     }

     Future<T> post<T>(String path, dynamic data) async {
       final response = await _dio.post(path, data: data);
       return response.data;
     }
   }
   ```

   **Provider (Riverpod)**:
   ```dart
   // lib/presentation/providers/auth_provider.dart
   import 'package:riverpod_annotation/riverpod_annotation.dart';

   part 'auth_provider.g.dart';

   @riverpod
   class Auth extends _$Auth {
     @override
     AsyncValue<User?> build() => const AsyncValue.data(null);

     Future<void> login(String username, String password) async {
       state = const AsyncValue.loading();
       state = await AsyncValue.guard(() async {
         final apiService = ref.read(apiServiceProvider);
         final response = await apiService.post('/api/v1/auth/login', {
           'username': username,
           'password': password,
         });
         return User.fromJson(response['data']['user']);
       });
     }

     void logout() {
       state = const AsyncValue.data(null);
     }
   }
   ```

   **Page Widget**:
   ```dart
   // lib/presentation/pages/login_page.dart
   import 'package:flutter/material.dart';
   import 'package:flutter_riverpod/flutter_riverpod.dart';

   class LoginPage extends ConsumerStatefulWidget {
     const LoginPage({super.key});

     @override
     ConsumerState<LoginPage> createState() => _LoginPageState();
   }

   class _LoginPageState extends ConsumerState<LoginPage> {
     final _usernameController = TextEditingController();
     final _passwordController = TextEditingController();

     @override
     Widget build(BuildContext context) {
       final authState = ref.watch(authProvider);

       return Scaffold(
         appBar: AppBar(title: const Text('登录')),
         body: Padding(
           padding: const EdgeInsets.all(16),
           child: Column(
             mainAxisAlignment: MainAxisAlignment.center,
             children: [
               TextField(
                 controller: _usernameController,
                 decoration: const InputDecoration(labelText: '用户名'),
               ),
               const SizedBox(height: 16),
               TextField(
                 controller: _passwordController,
                 obscureText: true,
                 decoration: const InputDecoration(labelText: '密码'),
               ),
               const SizedBox(height: 24),
               ElevatedButton(
                 onPressed: authState.isLoading
                     ? null
                     : () => ref.read(authProvider.notifier).login(
                           _usernameController.text,
                           _passwordController.text,
                         ),
                 child: authState.isLoading
                     ? const CircularProgressIndicator()
                     : const Text('登录'),
               ),
             ],
           ),
         ),
       );
     }
   }
   ```

3. **pubspec.yaml**:
   ```yaml
   dependencies:
     flutter:
       sdk: flutter
     flutter_riverpod: ^2.4.0
     riverpod_annotation: ^2.3.0
     dio: ^5.4.0
     go_router: ^13.0.0
     freezed_annotation: ^2.4.0
     json_annotation: ^4.8.0

   dev_dependencies:
     build_runner: ^2.4.0
     riverpod_generator: ^2.3.0
     freezed: ^2.4.0
     json_serializable: ^6.7.0
   ```

## Configuration

```yaml
tech_stack:
  flutter:
    dart_sdk: ">=3.0.0"
    state: riverpod
    network: dio
    router: go_router
```
