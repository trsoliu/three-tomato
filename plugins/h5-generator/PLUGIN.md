# H5/Web Generator Plugin

> Generate H5/Mobile Web code from requirement documents.

## Plugin Information

| Field | Value |
|-------|-------|
| Name | h5-generator |
| Version | 1.0.0 |
| Platform | H5/Mobile Web |
| Hooks | on_generate |

## Supported Tech Stacks

| Category | Options | Default |
|----------|---------|---------|
| Framework | Vue 3, Vue 2, React, Svelte | Vue 3 |
| Language | TypeScript, JavaScript | TypeScript |
| Bundler | Vite, Webpack, Rollup | Vite |
| UI | Vant, Antd Mobile, Element Plus | Vant |
| State | Pinia, Vuex, Redux, Zustand | Pinia |
| Router | Vue Router, React Router | Vue Router |
| CSS | SCSS, Less, Tailwind, CSS | SCSS |

## Hook: on_generate

### Instructions for AI Agent:

When generating H5/Web code:

1. **Read Configuration**
   - Check `tech_stack.h5` in config.yaml
   - Apply framework and library choices

2. **Project Structure (Vue 3 + Vite + Vant)**
   ```
   h5/
   ├── src/
   │   ├── api/
   │   │   ├── index.ts
   │   │   ├── auth.ts
   │   │   └── user.ts
   │   ├── assets/
   │   │   ├── images/
   │   │   └── styles/
   │   │       ├── variables.scss
   │   │       └── global.scss
   │   ├── components/
   │   │   └── common/
   │   │       └── AppButton.vue
   │   ├── composables/
   │   │   ├── useAuth.ts
   │   │   └── useRequest.ts
   │   ├── layouts/
   │   │   └── DefaultLayout.vue
   │   ├── router/
   │   │   └── index.ts
   │   ├── stores/
   │   │   ├── index.ts
   │   │   └── user.ts
   │   ├── types/
   │   │   ├── api.ts
   │   │   └── user.ts
   │   ├── utils/
   │   │   ├── request.ts
   │   │   └── storage.ts
   │   ├── views/
   │   │   ├── home/
   │   │   │   └── index.vue
   │   │   └── login/
   │   │       └── index.vue
   │   ├── App.vue
   │   └── main.ts
   ├── public/
   │   └── favicon.ico
   ├── index.html
   ├── vite.config.ts
   ├── tsconfig.json
   ├── package.json
   └── README.md
   ```

3. **Code Generation Rules**

   **Type Definitions**:
   ```typescript
   // types/user.ts
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
   
   // types/api.ts
   export interface ApiResponse<T> {
     code: number;
     message: string;
     data: T;
   }
   ```

   **Request Utility**:
   ```typescript
   // utils/request.ts
   import axios, { AxiosRequestConfig, AxiosResponse } from 'axios';
   import { showToast } from 'vant';
   import { getToken, removeToken } from './storage';
   import router from '@/router';
   
   const instance = axios.create({
     baseURL: import.meta.env.VITE_API_BASE_URL,
     timeout: 10000,
   });
   
   instance.interceptors.request.use((config) => {
     const token = getToken();
     if (token) {
       config.headers.Authorization = `Bearer ${token}`;
     }
     return config;
   });
   
   instance.interceptors.response.use(
     (response: AxiosResponse) => {
       const { code, message, data } = response.data;
       if (code === 0) {
         return data;
       }
       showToast(message);
       return Promise.reject(new Error(message));
     },
     (error) => {
       if (error.response?.status === 401) {
         removeToken();
         router.push('/login');
       }
       showToast(error.message);
       return Promise.reject(error);
     }
   );
   
   export const request = <T>(config: AxiosRequestConfig): Promise<T> => {
     return instance.request(config);
   };
   ```

   **API Service**:
   ```typescript
   // api/auth.ts
   import { request } from '@/utils/request';
   import type { User, LoginRequest } from '@/types/user';
   
   export const login = (data: LoginRequest) => {
     return request<{ token: string; user: User }>({
       url: '/api/v1/auth/login',
       method: 'POST',
       data,
     });
   };
   
   export const getUserInfo = () => {
     return request<User>({
       url: '/api/v1/user/info',
       method: 'GET',
     });
   };
   ```

   **Pinia Store**:
   ```typescript
   // stores/user.ts
   import { defineStore } from 'pinia';
   import { ref } from 'vue';
   import type { User } from '@/types/user';
   import { login as loginApi } from '@/api/auth';
   import { setToken, removeToken } from '@/utils/storage';
   
   export const useUserStore = defineStore('user', () => {
     const user = ref<User | null>(null);
     const isLoggedIn = ref(false);
   
     const login = async (username: string, password: string) => {
       const { token, user: userData } = await loginApi({ username, password });
       setToken(token);
       user.value = userData;
       isLoggedIn.value = true;
     };
   
     const logout = () => {
       removeToken();
       user.value = null;
       isLoggedIn.value = false;
     };
   
     return { user, isLoggedIn, login, logout };
   });
   ```

   **Vue Component**:
   ```vue
   <!-- views/login/index.vue -->
   <template>
     <div class="login-page">
       <van-form @submit="onSubmit">
         <van-cell-group inset>
           <van-field
             v-model="form.username"
             name="username"
             label="用户名"
             placeholder="请输入用户名"
             :rules="[{ required: true, message: '请填写用户名' }]"
           />
           <van-field
             v-model="form.password"
             type="password"
             name="password"
             label="密码"
             placeholder="请输入密码"
             :rules="[{ required: true, message: '请填写密码' }]"
           />
         </van-cell-group>
         
         <div class="submit-btn">
           <van-button 
             round 
             block 
             type="primary" 
             native-type="submit"
             :loading="loading"
           >
             登录
           </van-button>
         </div>
       </van-form>
     </div>
   </template>
   
   <script setup lang="ts">
   import { ref, reactive } from 'vue';
   import { useRouter } from 'vue-router';
   import { showToast } from 'vant';
   import { useUserStore } from '@/stores/user';
   
   const router = useRouter();
   const userStore = useUserStore();
   
   const loading = ref(false);
   const form = reactive({
     username: '',
     password: '',
   });
   
   const onSubmit = async () => {
     loading.value = true;
     try {
       await userStore.login(form.username, form.password);
       showToast('登录成功');
       router.push('/');
     } catch (error) {
       // Error handled by interceptor
     } finally {
       loading.value = false;
     }
   };
   </script>
   
   <style lang="scss" scoped>
   .login-page {
     min-height: 100vh;
     padding: 60px 16px;
     background: #f7f8fa;
   }
   
   .submit-btn {
     margin: 24px 16px;
   }
   </style>
   ```

   **Router Configuration**:
   ```typescript
   // router/index.ts
   import { createRouter, createWebHistory } from 'vue-router';
   import { getToken } from '@/utils/storage';
   
   const router = createRouter({
     history: createWebHistory(),
     routes: [
       {
         path: '/',
         component: () => import('@/views/home/index.vue'),
         meta: { requiresAuth: true },
       },
       {
         path: '/login',
         component: () => import('@/views/login/index.vue'),
       },
     ],
   });
   
   router.beforeEach((to, from, next) => {
     const token = getToken();
     if (to.meta.requiresAuth && !token) {
       next('/login');
     } else {
       next();
     }
   });
   
   export default router;
   ```

4. **Platform-Specific Considerations**
   - Mobile-first responsive design
   - Touch events and gestures
   - Safe area handling (notch, home indicator)
   - PWA support (optional)
   - WeChat/Alipay browser compatibility

5. **Dependencies** - package.json:
   ```json
   {
     "dependencies": {
       "vue": "^3.4.0",
       "vue-router": "^4.2.0",
       "pinia": "^2.1.0",
       "vant": "^4.8.0",
       "axios": "^1.6.0"
     },
     "devDependencies": {
       "@vitejs/plugin-vue": "^5.0.0",
       "vite": "^5.0.0",
       "typescript": "^5.3.0",
       "sass": "^1.69.0"
     }
   }
   ```

## Output Files

| File | Description |
|------|-------------|
| `package.json` | Dependencies |
| `vite.config.ts` | Vite config |
| `tsconfig.json` | TypeScript config |
| `src/` | Source code |
| `public/` | Static assets |
| `README.md` | Setup instructions |

## Configuration

```yaml
tech_stack:
  h5:
    framework: vue3
    language: typescript
    bundler: vite
    ui: vant
    state: pinia
    router: vue-router
    css: scss
```
