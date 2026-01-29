# Electron Generator Plugin

> Electron 桌面应用生成 (React + TypeScript)

## Plugin Information

| Field | Value |
|-------|-------|
| Name | electron-generator |
| Version | 1.0.0 |
| Platform | Electron (Windows, macOS, Linux) |
| Hooks | on_generate |

## AI 友好技术栈

| Category | Choice | Reason |
|----------|--------|--------|
| Frontend | React + TypeScript | AI 数据集最大 |
| Build | Vite + electron-vite | 快速构建 |
| State | Zustand | 轻量简洁 |
| UI | Ant Design | 组件丰富 |
| IPC | electron-trpc | 类型安全 |

## Hook: on_generate

### Instructions for AI Agent:

生成 Electron 代码时：

1. **项目结构**
   ```
   electron/
   ├── src/
   │   ├── main/                    # 主进程
   │   │   ├── index.ts
   │   │   └── ipc.ts
   │   ├── preload/                 # 预加载脚本
   │   │   └── index.ts
   │   └── renderer/                # 渲染进程 (React)
   │       ├── src/
   │       │   ├── App.tsx
   │       │   ├── main.tsx
   │       │   ├── components/
   │       │   ├── pages/
   │       │   ├── stores/
   │       │   ├── services/
   │       │   └── types/
   │       └── index.html
   ├── electron.vite.config.ts
   ├── package.json
   ├── tsconfig.json
   └── README.md
   ```

2. **代码示例**

   **主进程**:
   ```typescript
   // src/main/index.ts
   import { app, BrowserWindow, ipcMain } from 'electron';
   import path from 'path';

   let mainWindow: BrowserWindow | null = null;

   function createWindow() {
     mainWindow = new BrowserWindow({
       width: 1200,
       height: 800,
       webPreferences: {
         preload: path.join(__dirname, '../preload/index.js'),
         contextIsolation: true,
         nodeIntegration: false,
       },
     });

     if (process.env.NODE_ENV === 'development') {
       mainWindow.loadURL('http://localhost:5173');
       mainWindow.webContents.openDevTools();
     } else {
       mainWindow.loadFile(path.join(__dirname, '../renderer/index.html'));
     }
   }

   app.whenReady().then(createWindow);

   app.on('window-all-closed', () => {
     if (process.platform !== 'darwin') {
       app.quit();
     }
   });

   app.on('activate', () => {
     if (BrowserWindow.getAllWindows().length === 0) {
       createWindow();
     }
   });
   ```

   **预加载脚本**:
   ```typescript
   // src/preload/index.ts
   import { contextBridge, ipcRenderer } from 'electron';

   contextBridge.exposeInMainWorld('electronAPI', {
     getAppVersion: () => ipcRenderer.invoke('get-app-version'),
     openExternal: (url: string) => ipcRenderer.invoke('open-external', url),
     // 添加更多 API
   });
   ```

   **渲染进程 - Store**:
   ```typescript
   // src/renderer/src/stores/user.ts
   import { create } from 'zustand';
   import { persist } from 'zustand/middleware';
   import api from '../services/api';
   import type { User } from '../types';

   interface UserState {
     user: User | null;
     token: string | null;
     isLoading: boolean;
     login: (username: string, password: string) => Promise<void>;
     logout: () => void;
   }

   export const useUserStore = create<UserState>()(
     persist(
       (set) => ({
         user: null,
         token: null,
         isLoading: false,

         login: async (username, password) => {
           set({ isLoading: true });
           try {
             const response = await api.post('/api/v1/auth/login', {
               username,
               password,
             });
             const { token, user } = response.data.data;
             set({ token, user, isLoading: false });
           } catch (error) {
             set({ isLoading: false });
             throw error;
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

   **渲染进程 - Page**:
   ```tsx
   // src/renderer/src/pages/LoginPage.tsx
   import { useState } from 'react';
   import { Form, Input, Button, message, Card } from 'antd';
   import { UserOutlined, LockOutlined } from '@ant-design/icons';
   import { useUserStore } from '../stores/user';
   import { useNavigate } from 'react-router-dom';

   export function LoginPage() {
     const [loading, setLoading] = useState(false);
     const login = useUserStore((state) => state.login);
     const navigate = useNavigate();

     const onFinish = async (values: { username: string; password: string }) => {
       setLoading(true);
       try {
         await login(values.username, values.password);
         message.success('登录成功');
         navigate('/');
       } catch (error) {
         message.error('登录失败');
       } finally {
         setLoading(false);
       }
     };

     return (
       <div style={{ display: 'flex', justifyContent: 'center', alignItems: 'center', height: '100vh' }}>
         <Card title="登录" style={{ width: 400 }}>
           <Form onFinish={onFinish}>
             <Form.Item name="username" rules={[{ required: true, message: '请输入用户名' }]}>
               <Input prefix={<UserOutlined />} placeholder="用户名" />
             </Form.Item>
             <Form.Item name="password" rules={[{ required: true, message: '请输入密码' }]}>
               <Input.Password prefix={<LockOutlined />} placeholder="密码" />
             </Form.Item>
             <Form.Item>
               <Button type="primary" htmlType="submit" loading={loading} block>
                 登录
               </Button>
             </Form.Item>
           </Form>
         </Card>
       </div>
     );
   }
   ```

3. **package.json**:
   ```json
   {
     "name": "my-electron-app",
     "version": "1.0.0",
     "main": "dist/main/index.js",
     "scripts": {
       "dev": "electron-vite dev",
       "build": "electron-vite build",
       "preview": "electron-vite preview"
     },
     "dependencies": {
       "react": "^18.2.0",
       "react-dom": "^18.2.0",
       "react-router-dom": "^6.20.0",
       "antd": "^5.12.0",
       "zustand": "^4.4.0",
       "axios": "^1.6.0"
     },
     "devDependencies": {
       "electron": "^28.0.0",
       "electron-vite": "^2.0.0",
       "typescript": "^5.3.0",
       "@types/react": "^18.2.0"
     }
   }
   ```

## Configuration

```yaml
tech_stack:
  electron:
    frontend: react
    language: typescript
    build: electron-vite
    ui: antd
    state: zustand
```
