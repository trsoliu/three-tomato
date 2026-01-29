# WeChat Mini Program Generator Plugin

> Generate WeChat Mini Program code from requirement documents.

## Plugin Information

| Field | Value |
|-------|-------|
| Name | wechat-mp-generator |
| Version | 1.0.0 |
| Platform | 微信小程序 |
| Hooks | on_generate |

## Supported Tech Stacks

| Category | Options | Default |
|----------|---------|---------|
| Framework | Native, Taro, Uni-app | Native |
| Language | TypeScript, JavaScript | TypeScript |
| State | MobX, Redux, Vuex | MobX |
| UI | WeUI, Vant Weapp, TDesign | WeUI |
| Cloud | 是/否 | 否 |

## Hook: on_generate

### Instructions for AI Agent:

When generating WeChat Mini Program code:

1. **Read Configuration**
   - Check `tech_stack.wechat-mp` in config.yaml
   - Apply framework and UI library choices

2. **Project Structure (Native + TypeScript)**
   ```
   wechat-mp/
   ├── miniprogram/
   │   ├── pages/
   │   │   ├── index/
   │   │   │   ├── index.wxml
   │   │   │   ├── index.wxss
   │   │   │   ├── index.ts
   │   │   │   └── index.json
   │   │   └── login/
   │   │       ├── login.wxml
   │   │       ├── login.wxss
   │   │       ├── login.ts
   │   │       └── login.json
   │   ├── components/
   │   │   └── common-button/
   │   │       ├── index.wxml
   │   │       ├── index.wxss
   │   │       ├── index.ts
   │   │       └── index.json
   │   ├── services/
   │   │   ├── api.ts
   │   │   ├── auth.ts
   │   │   └── request.ts
   │   ├── models/
   │   │   ├── user.ts
   │   │   └── response.ts
   │   ├── stores/
   │   │   ├── index.ts
   │   │   └── user.ts
   │   ├── utils/
   │   │   ├── util.ts
   │   │   └── storage.ts
   │   ├── assets/
   │   │   └── images/
   │   ├── app.ts
   │   ├── app.json
   │   ├── app.wxss
   │   └── sitemap.json
   ├── typings/
   │   └── index.d.ts
   ├── project.config.json
   ├── project.private.config.json
   ├── tsconfig.json
   └── README.md
   ```

3. **Code Generation Rules**

   **Data Models**:
   ```typescript
   // models/user.ts
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

   **Request Utility**:
   ```typescript
   // services/request.ts
   const BASE_URL = 'https://api.example.com';
   
   interface RequestOptions {
     url: string;
     method?: 'GET' | 'POST' | 'PUT' | 'DELETE';
     data?: object;
     header?: object;
   }
   
   export const request = <T>(options: RequestOptions): Promise<T> => {
     return new Promise((resolve, reject) => {
       const token = wx.getStorageSync('token');
       
       wx.request({
         url: BASE_URL + options.url,
         method: options.method || 'GET',
         data: options.data,
         header: {
           'Content-Type': 'application/json',
           'Authorization': token ? `Bearer ${token}` : '',
           ...options.header
         },
         success: (res) => {
           if (res.statusCode === 200) {
             resolve(res.data as T);
           } else {
             reject(new Error(`请求失败: ${res.statusCode}`));
           }
         },
         fail: (err) => {
           reject(err);
         }
       });
     });
   };
   ```

   **Service Layer**:
   ```typescript
   // services/auth.ts
   import { request } from './request';
   import { User, LoginRequest, ApiResponse } from '../models/user';
   
   export const login = async (data: LoginRequest): Promise<User> => {
     const response = await request<ApiResponse<{ token: string; user: User }>>({
       url: '/api/v1/auth/login',
       method: 'POST',
       data
     });
     
     if (response.code === 0) {
       wx.setStorageSync('token', response.data.token);
       return response.data.user;
     }
     throw new Error(response.message);
   };
   ```

   **Page WXML**:
   ```html
   <!-- pages/login/login.wxml -->
   <view class="container">
     <view class="form">
       <input 
         class="input" 
         placeholder="用户名" 
         bindinput="onUsernameInput"
         value="{{username}}"
       />
       
       <input 
         class="input" 
         placeholder="密码" 
         password="{{true}}"
         bindinput="onPasswordInput"
         value="{{password}}"
       />
       
       <button 
         class="btn-login" 
         bindtap="onLogin"
         loading="{{isLoading}}"
         disabled="{{isLoading}}"
       >
         登录
       </button>
       
       <text wx:if="{{errorMessage}}" class="error">{{errorMessage}}</text>
     </view>
   </view>
   ```

   **Page TypeScript**:
   ```typescript
   // pages/login/login.ts
   import { login } from '../../services/auth';
   
   Page({
     data: {
       username: '',
       password: '',
       isLoading: false,
       errorMessage: ''
     },
     
     onUsernameInput(e: WechatMiniprogram.Input) {
       this.setData({ username: e.detail.value });
     },
     
     onPasswordInput(e: WechatMiniprogram.Input) {
       this.setData({ password: e.detail.value });
     },
     
     async onLogin() {
       const { username, password } = this.data;
       
       if (!username || !password) {
         this.setData({ errorMessage: '请填写完整信息' });
         return;
       }
       
       this.setData({ isLoading: true, errorMessage: '' });
       
       try {
         await login({ username, password });
         wx.switchTab({ url: '/pages/index/index' });
       } catch (error) {
         this.setData({ 
           errorMessage: (error as Error).message 
         });
       } finally {
         this.setData({ isLoading: false });
       }
     }
   });
   ```

   **Page WXSS**:
   ```css
   /* pages/login/login.wxss */
   .container {
     display: flex;
     flex-direction: column;
     align-items: center;
     justify-content: center;
     height: 100vh;
     padding: 0 40rpx;
   }
   
   .form {
     width: 100%;
   }
   
   .input {
     width: 100%;
     height: 88rpx;
     padding: 0 24rpx;
     margin-bottom: 24rpx;
     border: 1rpx solid #e5e5e5;
     border-radius: 8rpx;
     box-sizing: border-box;
   }
   
   .btn-login {
     width: 100%;
     height: 88rpx;
     line-height: 88rpx;
     background-color: #07c160;
     color: #fff;
     border-radius: 8rpx;
     margin-top: 40rpx;
   }
   
   .error {
     display: block;
     color: #fa5151;
     font-size: 24rpx;
     margin-top: 16rpx;
     text-align: center;
   }
   ```

4. **Platform-Specific Considerations**
   - Follow WeChat Mini Program lifecycle
   - Use `wx` API for platform capabilities
   - Handle authorization and permissions
   - Support sharing (onShareAppMessage)
   - Consider subscription messages

5. **app.json Configuration**:
   ```json
   {
     "pages": [
       "pages/index/index",
       "pages/login/login"
     ],
     "window": {
       "navigationBarTitleText": "My App",
       "navigationBarBackgroundColor": "#ffffff",
       "navigationBarTextStyle": "black"
     },
     "tabBar": {
       "list": [
         {
           "pagePath": "pages/index/index",
           "text": "首页"
         }
       ]
     }
   }
   ```

## Output Files

| File | Description |
|------|-------------|
| `project.config.json` | Project config |
| `miniprogram/app.json` | App config |
| `miniprogram/app.ts` | App entry |
| `miniprogram/pages/` | Pages |
| `miniprogram/components/` | Components |
| `miniprogram/services/` | Services |
| `README.md` | Setup instructions |

## Configuration

```yaml
tech_stack:
  wechat-mp:
    framework: native
    language: typescript
    state: mobx
    ui: weui
    cloud: false
```
