# Uni-app Generator Plugin

> Uni-app 跨端代码生成 (Vue 3 + TypeScript)

## Plugin Information

| Field | Value |
|-------|-------|
| Name | uni-app-generator |
| Version | 1.0.0 |
| Platform | Uni-app (小程序、H5、App) |
| Hooks | on_generate |

## AI 友好技术栈

| Category | Choice | Reason |
|----------|--------|--------|
| Framework | Vue 3 | 组合式 API，AI 友好 |
| Language | TypeScript | 类型安全 |
| State | Pinia | Vue 官方状态管理 |
| UI | uni-ui | 官方组件库 |
| Build | Vite | 快速构建 |

## Hook: on_generate

### Instructions for AI Agent:

生成 Uni-app 代码时：

1. **项目结构**
   ```
   uni-app/
   ├── src/
   │   ├── pages/
   │   │   ├── index/
   │   │   │   └── index.vue
   │   │   └── login/
   │   │       └── index.vue
   │   ├── components/
   │   ├── composables/
   │   │   └── useRequest.ts
   │   ├── stores/
   │   │   └── user.ts
   │   ├── services/
   │   │   └── api.ts
   │   ├── types/
   │   │   └── index.ts
   │   ├── utils/
   │   ├── static/
   │   ├── App.vue
   │   ├── main.ts
   │   ├── pages.json
   │   ├── manifest.json
   │   └── uni.scss
   ├── package.json
   ├── tsconfig.json
   ├── vite.config.ts
   └── README.md
   ```

2. **代码示例**

   **API Service**:
   ```typescript
   // src/services/api.ts
   const BASE_URL = 'https://api.example.com';

   interface RequestOptions {
     url: string;
     method?: 'GET' | 'POST' | 'PUT' | 'DELETE';
     data?: any;
   }

   export async function request<T>(options: RequestOptions): Promise<T> {
     const token = uni.getStorageSync('token');

     return new Promise((resolve, reject) => {
       uni.request({
         url: BASE_URL + options.url,
         method: options.method || 'GET',
         data: options.data,
         header: {
           'Content-Type': 'application/json',
           ...(token && { Authorization: `Bearer ${token}` }),
         },
         success: (res) => {
           if (res.statusCode === 200) {
             resolve(res.data as T);
           } else {
             reject(new Error(`请求失败: ${res.statusCode}`));
           }
         },
         fail: (err) => reject(err),
       });
     });
   }
   ```

   **Pinia Store**:
   ```typescript
   // src/stores/user.ts
   import { defineStore } from 'pinia';
   import { ref } from 'vue';
   import { request } from '@/services/api';
   import type { User, LoginRequest, ApiResponse } from '@/types';

   export const useUserStore = defineStore('user', () => {
     const user = ref<User | null>(null);
     const isLoading = ref(false);
     const error = ref<string | null>(null);

     async function login(data: LoginRequest) {
       isLoading.value = true;
       error.value = null;

       try {
         const response = await request<ApiResponse<{ token: string; user: User }>>({
           url: '/api/v1/auth/login',
           method: 'POST',
           data,
         });

         if (response.code === 0) {
           uni.setStorageSync('token', response.data.token);
           user.value = response.data.user;
           uni.switchTab({ url: '/pages/index/index' });
         } else {
           error.value = response.message;
         }
       } catch (e) {
         error.value = (e as Error).message;
       } finally {
         isLoading.value = false;
       }
     }

     function logout() {
       uni.removeStorageSync('token');
       user.value = null;
       uni.reLaunch({ url: '/pages/login/index' });
     }

     return { user, isLoading, error, login, logout };
   });
   ```

   **Page Component**:
   ```vue
   <!-- src/pages/login/index.vue -->
   <template>
     <view class="container">
       <view class="form">
         <uni-easyinput
           v-model="form.username"
           placeholder="请输入用户名"
         />
         <uni-easyinput
           v-model="form.password"
           type="password"
           placeholder="请输入密码"
         />
         <text v-if="userStore.error" class="error">
           {{ userStore.error }}
         </text>
         <button
           type="primary"
           :loading="userStore.isLoading"
           :disabled="userStore.isLoading"
           @click="handleLogin"
         >
           登录
         </button>
       </view>
     </view>
   </template>

   <script setup lang="ts">
   import { reactive } from 'vue';
   import { useUserStore } from '@/stores/user';

   const userStore = useUserStore();

   const form = reactive({
     username: '',
     password: '',
   });

   function handleLogin() {
     if (!form.username || !form.password) {
       uni.showToast({ title: '请填写完整信息', icon: 'none' });
       return;
     }
     userStore.login(form);
   }
   </script>

   <style lang="scss" scoped>
   .container {
     padding: 40rpx;
   }
   .form {
     display: flex;
     flex-direction: column;
     gap: 24rpx;
   }
   .error {
     color: #f56c6c;
     font-size: 24rpx;
   }
   </style>
   ```

3. **pages.json**:
   ```json
   {
     "pages": [
       { "path": "pages/index/index" },
       { "path": "pages/login/index" }
     ],
     "globalStyle": {
       "navigationBarTitleText": "My App"
     }
   }
   ```

## Configuration

```yaml
tech_stack:
  uni-app:
    vue_version: 3
    language: typescript
    state: pinia
    ui: uni-ui
    compiler: vite
```
