# Web Desktop Generator Plugin

> 生成 Web 桌面端原生代码 (Next.js + React + TypeScript)

## Plugin Information

| Field | Value |
|-------|-------|
| Name | web-generator |
| Version | 1.0.0 |
| Platform | Web Desktop |
| Hooks | on_generate |

## AI 友好技术栈

| Category | Choice | Reason |
|----------|--------|--------|
| Framework | React | AI 数据集最大，生态最成熟 |
| Meta Framework | Next.js | SSR/SSG，企业级首选 |
| Language | TypeScript | 类型安全，AI 友好 |
| UI | Ant Design / shadcn/ui | 组件丰富，文档完善 |
| State | Zustand | 轻量简洁，AI 易理解 |
| CSS | Tailwind CSS | 原子化，AI 友好 |

## Hook: on_generate

### Instructions for AI Agent:

生成 Web 桌面端代码时：

1. **项目结构 (Next.js 14 App Router)**
   ```
   web/
   ├── src/
   │   ├── app/                    # App Router
   │   │   ├── layout.tsx
   │   │   ├── page.tsx
   │   │   ├── (auth)/
   │   │   │   ├── login/
   │   │   │   └── register/
   │   │   └── (dashboard)/
   │   │       ├── layout.tsx
   │   │       └── page.tsx
   │   ├── components/
   │   │   ├── ui/                 # 基础 UI 组件
   │   │   └── features/           # 业务组件
   │   ├── lib/
   │   │   ├── api.ts              # API 客户端
   │   │   ├── auth.ts             # 认证逻辑
   │   │   └── utils.ts
   │   ├── hooks/                  # 自定义 Hooks
   │   ├── stores/                 # Zustand stores
   │   ├── types/                  # TypeScript 类型
   │   └── styles/
   │       └── globals.css
   ├── public/
   ├── next.config.js
   ├── tailwind.config.ts
   ├── tsconfig.json
   ├── package.json
   └── README.md
   ```

2. **代码示例**

   **API 客户端**:
   ```typescript
   // src/lib/api.ts
   const BASE_URL = process.env.NEXT_PUBLIC_API_URL;

   export async function fetchApi<T>(
     endpoint: string,
     options?: RequestInit
   ): Promise<T> {
     const token = typeof window !== 'undefined' 
       ? localStorage.getItem('token') 
       : null;

     const res = await fetch(`${BASE_URL}${endpoint}`, {
       ...options,
       headers: {
         'Content-Type': 'application/json',
         ...(token && { Authorization: `Bearer ${token}` }),
         ...options?.headers,
       },
     });

     if (!res.ok) {
       throw new Error(`API Error: ${res.status}`);
     }

     return res.json();
   }
   ```

   **Zustand Store**:
   ```typescript
   // src/stores/user.ts
   import { create } from 'zustand';
   import { persist } from 'zustand/middleware';

   interface User {
     id: string;
     username: string;
     avatar?: string;
   }

   interface UserStore {
     user: User | null;
     isLoggedIn: boolean;
     setUser: (user: User) => void;
     logout: () => void;
   }

   export const useUserStore = create<UserStore>()(
     persist(
       (set) => ({
         user: null,
         isLoggedIn: false,
         setUser: (user) => set({ user, isLoggedIn: true }),
         logout: () => set({ user: null, isLoggedIn: false }),
       }),
       { name: 'user-storage' }
     )
   );
   ```

   **Server Component (Next.js)**:
   ```typescript
   // src/app/(dashboard)/page.tsx
   import { fetchApi } from '@/lib/api';

   async function getData() {
     return fetchApi<{ items: Item[] }>('/api/items');
   }

   export default async function DashboardPage() {
     const data = await getData();

     return (
       <main className="container mx-auto p-6">
         <h1 className="text-2xl font-bold mb-4">Dashboard</h1>
         {/* 渲染数据 */}
       </main>
     );
   }
   ```

   **Client Component**:
   ```typescript
   'use client';

   import { useState } from 'react';
   import { Button } from '@/components/ui/button';

   export function LoginForm() {
     const [username, setUsername] = useState('');
     const [password, setPassword] = useState('');

     const handleSubmit = async (e: React.FormEvent) => {
       e.preventDefault();
       // 登录逻辑
     };

     return (
       <form onSubmit={handleSubmit} className="space-y-4">
         <input
           type="text"
           value={username}
           onChange={(e) => setUsername(e.target.value)}
           className="w-full px-4 py-2 border rounded"
           placeholder="用户名"
         />
         <input
           type="password"
           value={password}
           onChange={(e) => setPassword(e.target.value)}
           className="w-full px-4 py-2 border rounded"
           placeholder="密码"
         />
         <Button type="submit" className="w-full">
           登录
         </Button>
       </form>
     );
   }
   ```

3. **Dependencies (package.json)**:
   ```json
   {
     "dependencies": {
       "next": "^14.0.0",
       "react": "^18.2.0",
       "react-dom": "^18.2.0",
       "zustand": "^4.4.0",
       "antd": "^5.12.0"
     },
     "devDependencies": {
       "typescript": "^5.3.0",
       "tailwindcss": "^3.4.0",
       "@types/react": "^18.2.0",
       "@types/node": "^20.0.0"
     }
   }
   ```

## Configuration

```yaml
tech_stack:
  web:
    framework: react
    meta_framework: nextjs
    language: typescript
    ui: antd
    state: zustand
    css: tailwindcss
```
