# Taro Generator Plugin

> Taro 跨端代码生成 (React + TypeScript)

## Plugin Information

| Field | Value |
|-------|-------|
| Name | taro-generator |
| Version | 1.0.0 |
| Platform | Taro (小程序、H5、RN) |
| Hooks | on_generate |

## AI 友好技术栈

| Category | Choice | Reason |
|----------|--------|--------|
| Framework | React | AI 数据集最大 |
| Language | TypeScript | 类型安全 |
| State | Zustand | 轻量简洁 |
| UI | NutUI | 京东官方组件 |

## Hook: on_generate

### Instructions for AI Agent:

生成 Taro 代码时：

1. **项目结构**
   ```
   taro/
   ├── src/
   │   ├── pages/
   │   │   ├── index/
   │   │   │   ├── index.tsx
   │   │   │   └── index.scss
   │   │   └── login/
   │   │       ├── index.tsx
   │   │       └── index.scss
   │   ├── components/
   │   ├── services/
   │   │   └── api.ts
   │   ├── stores/
   │   │   └── user.ts
   │   ├── types/
   │   ├── utils/
   │   ├── app.tsx
   │   ├── app.scss
   │   └── app.config.ts
   ├── config/
   ├── package.json
   ├── tsconfig.json
   └── README.md
   ```

2. **代码示例**

   **API Service**:
   ```typescript
   // src/services/api.ts
   import Taro from '@tarojs/taro';

   const BASE_URL = 'https://api.example.com';

   export async function request<T>(options: {
     url: string;
     method?: 'GET' | 'POST';
     data?: any;
   }): Promise<T> {
     const token = Taro.getStorageSync('token');

     const response = await Taro.request({
       url: BASE_URL + options.url,
       method: options.method || 'GET',
       data: options.data,
       header: {
         'Content-Type': 'application/json',
         ...(token && { Authorization: `Bearer ${token}` }),
       },
     });

     if (response.statusCode === 200) {
       return response.data as T;
     }
     throw new Error(`请求失败: ${response.statusCode}`);
   }
   ```

   **Zustand Store**:
   ```typescript
   // src/stores/user.ts
   import { create } from 'zustand';
   import Taro from '@tarojs/taro';
   import { request } from '@/services/api';
   import type { User, ApiResponse } from '@/types';

   interface UserState {
     user: User | null;
     isLoading: boolean;
     error: string | null;
     login: (username: string, password: string) => Promise<void>;
     logout: () => void;
   }

   export const useUserStore = create<UserState>((set) => ({
     user: null,
     isLoading: false,
     error: null,

     login: async (username, password) => {
       set({ isLoading: true, error: null });
       try {
         const res = await request<ApiResponse<{ token: string; user: User }>>({
           url: '/api/v1/auth/login',
           method: 'POST',
           data: { username, password },
         });

         if (res.code === 0) {
           Taro.setStorageSync('token', res.data.token);
           set({ user: res.data.user, isLoading: false });
           Taro.switchTab({ url: '/pages/index/index' });
         } else {
           set({ error: res.message, isLoading: false });
         }
       } catch (e) {
         set({ error: (e as Error).message, isLoading: false });
       }
     },

     logout: () => {
       Taro.removeStorageSync('token');
       set({ user: null });
       Taro.reLaunch({ url: '/pages/login/index' });
     },
   }));
   ```

   **Page Component**:
   ```tsx
   // src/pages/login/index.tsx
   import { useState } from 'react';
   import { View, Input, Button, Text } from '@tarojs/components';
   import { useUserStore } from '@/stores/user';
   import './index.scss';

   export default function LoginPage() {
     const [username, setUsername] = useState('');
     const [password, setPassword] = useState('');
     const { login, isLoading, error } = useUserStore();

     const handleLogin = () => {
       if (!username || !password) {
         Taro.showToast({ title: '请填写完整信息', icon: 'none' });
         return;
       }
       login(username, password);
     };

     return (
       <View className="login-page">
         <Input
           className="input"
           placeholder="用户名"
           value={username}
           onInput={(e) => setUsername(e.detail.value)}
         />
         <Input
           className="input"
           type="password"
           placeholder="密码"
           value={password}
           onInput={(e) => setPassword(e.detail.value)}
         />
         {error && <Text className="error">{error}</Text>}
         <Button
           className="btn"
           type="primary"
           loading={isLoading}
           disabled={isLoading}
           onClick={handleLogin}
         >
           登录
         </Button>
       </View>
     );
   }
   ```

3. **app.config.ts**:
   ```typescript
   export default defineAppConfig({
     pages: [
       'pages/index/index',
       'pages/login/index',
     ],
     window: {
       navigationBarTitleText: 'My App',
     },
   });
   ```

## Configuration

```yaml
tech_stack:
  taro:
    version: 3
    framework: react
    language: typescript
    state: zustand
    ui: nutui
```
