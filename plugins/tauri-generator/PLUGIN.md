# Tauri Generator Plugin

> Tauri 桌面应用生成 (Rust + React)

## Plugin Information

| Field | Value |
|-------|-------|
| Name | tauri-generator |
| Version | 1.0.0 |
| Platform | Tauri (Windows, macOS, Linux) |
| Hooks | on_generate |

## AI 友好技术栈

| Category | Choice | Reason |
|----------|--------|--------|
| Backend | Rust | 高性能，内存安全 |
| Frontend | React + TypeScript | AI 数据集最大 |
| Build | Vite | 快速构建 |
| State | Zustand | 轻量简洁 |
| UI | shadcn/ui + Tailwind | 现代 UI |

## Hook: on_generate

### Instructions for AI Agent:

生成 Tauri 代码时：

1. **项目结构**
   ```
   tauri/
   ├── src/                        # React 前端
   │   ├── App.tsx
   │   ├── main.tsx
   │   ├── components/
   │   │   └── ui/                 # shadcn/ui 组件
   │   ├── pages/
   │   │   ├── LoginPage.tsx
   │   │   └── HomePage.tsx
   │   ├── stores/
   │   │   └── user.ts
   │   ├── services/
   │   │   └── api.ts
   │   ├── lib/
   │   │   └── utils.ts
   │   └── types/
   ├── src-tauri/                  # Rust 后端
   │   ├── src/
   │   │   ├── main.rs
   │   │   ├── lib.rs
   │   │   └── commands/
   │   │       └── mod.rs
   │   ├── Cargo.toml
   │   ├── tauri.conf.json
   │   └── icons/
   ├── index.html
   ├── package.json
   ├── vite.config.ts
   ├── tailwind.config.js
   └── README.md
   ```

2. **代码示例**

   **Rust 后端 - Commands**:
   ```rust
   // src-tauri/src/commands/mod.rs
   use serde::{Deserialize, Serialize};
   use tauri::command;

   #[derive(Debug, Serialize, Deserialize)]
   pub struct User {
       pub id: String,
       pub username: String,
       pub avatar: Option<String>,
   }

   #[derive(Debug, Deserialize)]
   pub struct LoginRequest {
       pub username: String,
       pub password: String,
   }

   #[derive(Debug, Serialize)]
   pub struct LoginResponse {
       pub token: String,
       pub user: User,
   }

   #[command]
   pub async fn login(request: LoginRequest) -> Result<LoginResponse, String> {
       // 调用 API 或本地验证
       let client = reqwest::Client::new();
       let response = client
           .post("https://api.example.com/api/v1/auth/login")
           .json(&request)
           .send()
           .await
           .map_err(|e| e.to_string())?;

       let data: serde_json::Value = response.json().await.map_err(|e| e.to_string())?;
       
       if data["code"].as_i64() == Some(0) {
           Ok(LoginResponse {
               token: data["data"]["token"].as_str().unwrap_or("").to_string(),
               user: User {
                   id: data["data"]["user"]["id"].as_str().unwrap_or("").to_string(),
                   username: data["data"]["user"]["username"].as_str().unwrap_or("").to_string(),
                   avatar: data["data"]["user"]["avatar"].as_str().map(|s| s.to_string()),
               },
           })
       } else {
           Err(data["message"].as_str().unwrap_or("登录失败").to_string())
       }
   }

   #[command]
   pub fn greet(name: &str) -> String {
       format!("Hello, {}!", name)
   }
   ```

   **Rust 后端 - Main**:
   ```rust
   // src-tauri/src/main.rs
   #![cfg_attr(not(debug_assertions), windows_subsystem = "windows")]

   mod commands;

   use commands::{greet, login};

   fn main() {
       tauri::Builder::default()
           .invoke_handler(tauri::generate_handler![greet, login])
           .run(tauri::generate_context!())
           .expect("error while running tauri application");
   }
   ```

   **React 前端 - Store**:
   ```typescript
   // src/stores/user.ts
   import { create } from 'zustand';
   import { persist } from 'zustand/middleware';
   import { invoke } from '@tauri-apps/api/tauri';

   interface User {
     id: string;
     username: string;
     avatar?: string;
   }

   interface UserState {
     user: User | null;
     token: string | null;
     isLoading: boolean;
     error: string | null;
     login: (username: string, password: string) => Promise<void>;
     logout: () => void;
   }

   export const useUserStore = create<UserState>()(
     persist(
       (set) => ({
         user: null,
         token: null,
         isLoading: false,
         error: null,

         login: async (username, password) => {
           set({ isLoading: true, error: null });
           try {
             const response = await invoke<{ token: string; user: User }>('login', {
               request: { username, password },
             });
             set({ token: response.token, user: response.user, isLoading: false });
           } catch (error) {
             set({ error: error as string, isLoading: false });
           }
         },

         logout: () => {
           set({ user: null, token: null });
         },
       }),
       { name: 'user-storage' }
     )
   );
   ```

   **React 前端 - Page**:
   ```tsx
   // src/pages/LoginPage.tsx
   import { useState } from 'react';
   import { useNavigate } from 'react-router-dom';
   import { Button } from '@/components/ui/button';
   import { Input } from '@/components/ui/input';
   import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
   import { useUserStore } from '@/stores/user';

   export function LoginPage() {
     const [username, setUsername] = useState('');
     const [password, setPassword] = useState('');
     const { login, isLoading, error } = useUserStore();
     const navigate = useNavigate();

     const handleSubmit = async (e: React.FormEvent) => {
       e.preventDefault();
       await login(username, password);
       if (!error) {
         navigate('/');
       }
     };

     return (
       <div className="flex items-center justify-center min-h-screen">
         <Card className="w-[400px]">
           <CardHeader>
             <CardTitle>登录</CardTitle>
           </CardHeader>
           <CardContent>
             <form onSubmit={handleSubmit} className="space-y-4">
               <Input
                 placeholder="用户名"
                 value={username}
                 onChange={(e) => setUsername(e.target.value)}
               />
               <Input
                 type="password"
                 placeholder="密码"
                 value={password}
                 onChange={(e) => setPassword(e.target.value)}
               />
               {error && <p className="text-red-500 text-sm">{error}</p>}
               <Button type="submit" className="w-full" disabled={isLoading}>
                 {isLoading ? '登录中...' : '登录'}
               </Button>
             </form>
           </CardContent>
         </Card>
       </div>
     );
   }
   ```

3. **Cargo.toml**:
   ```toml
   [package]
   name = "my-tauri-app"
   version = "1.0.0"
   edition = "2021"

   [dependencies]
   tauri = { version = "1.5", features = ["shell-open"] }
   serde = { version = "1.0", features = ["derive"] }
   serde_json = "1.0"
   reqwest = { version = "0.11", features = ["json"] }
   tokio = { version = "1", features = ["full"] }

   [build-dependencies]
   tauri-build = { version = "1.5" }
   ```

4. **package.json**:
   ```json
   {
     "dependencies": {
       "react": "^18.2.0",
       "react-dom": "^18.2.0",
       "react-router-dom": "^6.20.0",
       "zustand": "^4.4.0",
       "@tauri-apps/api": "^1.5.0"
     },
     "devDependencies": {
       "@tauri-apps/cli": "^1.5.0",
       "vite": "^5.0.0",
       "typescript": "^5.3.0",
       "tailwindcss": "^3.4.0"
     }
   }
   ```

## Configuration

```yaml
tech_stack:
  tauri:
    backend: rust
    frontend: react
    language: typescript
    build: vite
    ui: shadcn-ui
    css: tailwindcss
```
