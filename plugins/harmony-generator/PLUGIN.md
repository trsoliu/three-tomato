# HarmonyOS Generator Plugin

> Generate HarmonyOS code from requirement documents.

## Plugin Information

| Field | Value |
|-------|-------|
| Name | harmony-generator |
| Version | 1.0.0 |
| Platform | HarmonyOS |
| Hooks | on_generate |

## Supported Tech Stacks

| Category | Options | Default |
|----------|---------|---------|
| Language | ArkTS, eTS | ArkTS |
| API Version | 9, 10, 11 | 11 |
| UI | ArkUI | ArkUI |
| Architecture | MVVM | MVVM |
| Network | @ohos/axios, http | http |
| Database | Preferences, RelationalStore | Preferences |

## Hook: on_generate

### Instructions for AI Agent:

When generating HarmonyOS code:

1. **Read Configuration**
   - Check `tech_stack.harmony` in config.yaml
   - Apply API version and architecture choices

2. **Project Structure (ArkTS + ArkUI)**
   ```
   harmony/
   ├── entry/
   │   └── src/main/
   │       ├── ets/
   │       │   ├── entryability/
   │       │   │   └── EntryAbility.ets
   │       │   ├── pages/
   │       │   │   ├── Index.ets
   │       │   │   └── Login.ets
   │       │   ├── components/
   │       │   │   └── CommonButton.ets
   │       │   ├── viewmodel/
   │       │   │   └── LoginViewModel.ets
   │       │   ├── model/
   │       │   │   ├── User.ets
   │       │   │   └── ApiResponse.ets
   │       │   ├── service/
   │       │   │   ├── HttpUtil.ets
   │       │   │   └── AuthService.ets
   │       │   ├── common/
   │       │   │   ├── constants/
   │       │   │   └── utils/
   │       │   └── resources/
   │       ├── resources/
   │       │   ├── base/
   │       │   │   ├── element/
   │       │   │   │   └── string.json
   │       │   │   ├── media/
   │       │   │   └── profile/
   │       │   └── rawfile/
   │       └── module.json5
   ├── oh-package.json5
   ├── build-profile.json5
   ├── hvigorfile.ts
   └── README.md
   ```

3. **Code Generation Rules**

   **Data Models** - Convert from requirement:
   ```typescript
   // From requirement: User entity
   export interface User {
     id: string;
     username: string;
     avatar?: string;
     createdAt: string;
   }
   
   export interface LoginRequest {
     username: string;
     password: string;
   }
   
   export interface ApiResponse<T> {
     code: number;
     message: string;
     data: T;
   }
   ```

   **HTTP Utility**:
   ```typescript
   import http from '@ohos.net.http';
   
   class HttpUtil {
     private baseUrl: string = 'https://api.example.com';
     
     async post<T>(path: string, data: object): Promise<T> {
       const httpRequest = http.createHttp();
       try {
         const response = await httpRequest.request(
           this.baseUrl + path,
           {
             method: http.RequestMethod.POST,
             header: { 'Content-Type': 'application/json' },
             extraData: JSON.stringify(data)
           }
         );
         return JSON.parse(response.result as string) as T;
       } finally {
         httpRequest.destroy();
       }
     }
   }
   
   export default new HttpUtil();
   ```

   **Service Layer**:
   ```typescript
   import HttpUtil from '../common/HttpUtil';
   import { User, LoginRequest, ApiResponse } from '../model/User';
   
   class AuthService {
     async login(request: LoginRequest): Promise<User> {
       const response = await HttpUtil.post<ApiResponse<{ user: User }>>(
         '/api/v1/auth/login',
         request
       );
       if (response.code === 0) {
         return response.data.user;
       }
       throw new Error(response.message);
     }
   }
   
   export default new AuthService();
   ```

   **ViewModel**:
   ```typescript
   import AuthService from '../service/AuthService';
   import { User } from '../model/User';
   
   @Observed
   export class LoginViewModel {
     username: string = '';
     password: string = '';
     isLoading: boolean = false;
     errorMessage: string = '';
     
     async login(): Promise<User | null> {
       this.isLoading = true;
       this.errorMessage = '';
       
       try {
         const user = await AuthService.login({
           username: this.username,
           password: this.password
         });
         return user;
       } catch (error) {
         this.errorMessage = (error as Error).message;
         return null;
       } finally {
         this.isLoading = false;
       }
     }
   }
   ```

   **ArkUI Page**:
   ```typescript
   import router from '@ohos.router';
   import { LoginViewModel } from '../viewmodel/LoginViewModel';
   
   @Entry
   @Component
   struct LoginPage {
     @State viewModel: LoginViewModel = new LoginViewModel();
     
     build() {
       Column() {
         TextInput({ placeholder: '用户名' })
           .width('80%')
           .height(50)
           .onChange((value: string) => {
             this.viewModel.username = value;
           })
         
         TextInput({ placeholder: '密码' })
           .type(InputType.Password)
           .width('80%')
           .height(50)
           .margin({ top: 20 })
           .onChange((value: string) => {
             this.viewModel.password = value;
           })
         
         Button('登录')
           .width('80%')
           .height(50)
           .margin({ top: 30 })
           .onClick(async () => {
             const user = await this.viewModel.login();
             if (user) {
               router.pushUrl({ url: 'pages/Home' });
             }
           })
         
         if (this.viewModel.errorMessage) {
           Text(this.viewModel.errorMessage)
             .fontColor(Color.Red)
             .margin({ top: 10 })
         }
       }
       .width('100%')
       .height('100%')
       .justifyContent(FlexAlign.Center)
     }
   }
   ```

4. **Platform-Specific Considerations**
   - Use `@ohos` APIs for system capabilities
   - Handle Ability lifecycle properly
   - Support dark mode via `@ohos.app.ability.Configuration`
   - Consider foldable device layouts
   - Handle permissions properly

5. **Dependencies** - Add to oh-package.json5:
   ```json5
   {
     "dependencies": {
       "@ohos/axios": "^2.0.0"
     }
   }
   ```

## Output Files

| File | Description |
|------|-------------|
| `build-profile.json5` | Build configuration |
| `oh-package.json5` | Package manifest |
| `entry/src/main/ets/` | Source code |
| `entry/src/main/resources/` | Resources |
| `entry/src/main/module.json5` | Module config |
| `README.md` | Setup instructions |

## Configuration

```yaml
tech_stack:
  harmony:
    language: arkts
    api_version: 11
    ui: arkui
    architecture: mvvm
    network: http
    database: preferences
```
