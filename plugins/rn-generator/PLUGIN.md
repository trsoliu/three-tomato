# React Native Generator Plugin

> React Native 跨端代码生成 (TypeScript + Zustand)

## Plugin Information

| Field | Value |
|-------|-------|
| Name | rn-generator |
| Version | 1.0.0 |
| Platform | React Native (iOS, Android) |
| Hooks | on_generate |

## AI 友好技术栈

| Category | Choice | Reason |
|----------|--------|--------|
| Language | TypeScript | 类型安全，AI 数据集大 |
| State | Zustand | 轻量简洁，AI 友好 |
| Navigation | React Navigation | 最成熟的方案 |
| Network | Axios | 文档丰富 |
| UI | React Native Paper | Material Design |

## Hook: on_generate

### Instructions for AI Agent:

生成 React Native 代码时：

1. **项目结构**
   ```
   react-native/
   ├── src/
   │   ├── App.tsx
   │   ├── components/
   │   │   └── common/
   │   ├── screens/
   │   │   ├── LoginScreen.tsx
   │   │   └── HomeScreen.tsx
   │   ├── navigation/
   │   │   └── AppNavigator.tsx
   │   ├── services/
   │   │   └── api.ts
   │   ├── stores/
   │   │   └── useAuthStore.ts
   │   ├── types/
   │   │   └── index.ts
   │   └── utils/
   ├── package.json
   ├── tsconfig.json
   └── README.md
   ```

2. **代码示例**

   **类型定义**:
   ```typescript
   // src/types/index.ts
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

   **API Service**:
   ```typescript
   // src/services/api.ts
   import axios from 'axios';
   import AsyncStorage from '@react-native-async-storage/async-storage';

   const api = axios.create({
     baseURL: 'https://api.example.com',
     timeout: 10000,
   });

   api.interceptors.request.use(async (config) => {
     const token = await AsyncStorage.getItem('token');
     if (token) {
       config.headers.Authorization = `Bearer ${token}`;
     }
     return config;
   });

   export default api;
   ```

   **Zustand Store**:
   ```typescript
   // src/stores/useAuthStore.ts
   import { create } from 'zustand';
   import AsyncStorage from '@react-native-async-storage/async-storage';
   import api from '../services/api';
   import type { User, LoginRequest, ApiResponse } from '../types';

   interface AuthState {
     user: User | null;
     isLoading: boolean;
     error: string | null;
     login: (data: LoginRequest) => Promise<void>;
     logout: () => Promise<void>;
   }

   export const useAuthStore = create<AuthState>((set) => ({
     user: null,
     isLoading: false,
     error: null,

     login: async (data) => {
       set({ isLoading: true, error: null });
       try {
         const response = await api.post<ApiResponse<{ token: string; user: User }>>(
           '/api/v1/auth/login',
           data
         );
         if (response.data.code === 0) {
           await AsyncStorage.setItem('token', response.data.data.token);
           set({ user: response.data.data.user, isLoading: false });
         } else {
           set({ error: response.data.message, isLoading: false });
         }
       } catch (error) {
         set({ error: (error as Error).message, isLoading: false });
       }
     },

     logout: async () => {
       await AsyncStorage.removeItem('token');
       set({ user: null });
     },
   }));
   ```

   **Screen Component**:
   ```typescript
   // src/screens/LoginScreen.tsx
   import React, { useState } from 'react';
   import { View, StyleSheet } from 'react-native';
   import { TextInput, Button, Text } from 'react-native-paper';
   import { useAuthStore } from '../stores/useAuthStore';

   export function LoginScreen() {
     const [username, setUsername] = useState('');
     const [password, setPassword] = useState('');
     const { login, isLoading, error } = useAuthStore();

     const handleLogin = () => {
       login({ username, password });
     };

     return (
       <View style={styles.container}>
         <TextInput
           label="用户名"
           value={username}
           onChangeText={setUsername}
           style={styles.input}
         />
         <TextInput
           label="密码"
           value={password}
           onChangeText={setPassword}
           secureTextEntry
           style={styles.input}
         />
         {error && <Text style={styles.error}>{error}</Text>}
         <Button
           mode="contained"
           onPress={handleLogin}
           loading={isLoading}
           disabled={isLoading}
         >
           登录
         </Button>
       </View>
     );
   }

   const styles = StyleSheet.create({
     container: {
       flex: 1,
       padding: 16,
       justifyContent: 'center',
     },
     input: {
       marginBottom: 16,
     },
     error: {
       color: 'red',
       marginBottom: 16,
     },
   });
   ```

3. **package.json**:
   ```json
   {
     "dependencies": {
       "react": "18.2.0",
       "react-native": "0.73.0",
       "@react-navigation/native": "^6.1.0",
       "@react-navigation/native-stack": "^6.9.0",
       "react-native-paper": "^5.11.0",
       "zustand": "^4.4.0",
       "axios": "^1.6.0",
       "@react-native-async-storage/async-storage": "^1.21.0"
     }
   }
   ```

## Configuration

```yaml
tech_stack:
  react-native:
    version: "0.73"
    language: typescript
    state: zustand
    navigation: react-navigation
    ui: paper
```
