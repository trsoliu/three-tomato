# Quick App Generator Plugin

> Generate Quick App (快应用) code from requirement documents.

## Plugin Information

| Field | Value |
|-------|-------|
| Name | quick-app-generator |
| Version | 1.0.0 |
| Platform | 快应用 |
| Hooks | on_generate |

## Supported Tech Stacks

| Category | Options | Default |
|----------|---------|---------|
| Min Platform | 1070+ | 1070 |
| Language | TypeScript, JavaScript | TypeScript |
| UI | Custom | Custom |

## Hook: on_generate

### Instructions for AI Agent:

When generating Quick App code:

1. **Read Configuration**
   - Check `tech_stack.quick-app` in config.yaml

2. **Project Structure**
   ```
   quick-app/
   ├── src/
   │   ├── pages/
   │   │   ├── Index/
   │   │   │   └── index.ux
   │   │   └── Login/
   │   │       └── index.ux
   │   ├── components/
   │   ├── services/
   │   ├── utils/
   │   ├── app.ux
   │   └── manifest.json
   ├── sign/
   │   └── debug/
   ├── package.json
   └── README.md
   ```

3. **Key Features**
   - Uses `.ux` files (similar to Vue SFC)
   - Native-like performance
   - System-level integration
   - No installation required

4. **Code Example**:
   ```html
   <!-- src/pages/Login/index.ux -->
   <template>
     <div class="container">
       <input 
         type="text" 
         placeholder="用户名"
         value="{{username}}"
         onchange="onUsernameChange"
       />
       <input 
         type="password"
         placeholder="密码"
         value="{{password}}"
         onchange="onPasswordChange"
       />
       <input 
         type="button" 
         value="登录"
         onclick="onLogin"
       />
     </div>
   </template>
   
   <script>
   import fetch from '@system.fetch';
   import router from '@system.router';
   import prompt from '@system.prompt';
   
   export default {
     data: {
       username: '',
       password: ''
     },
     
     onUsernameChange(e) {
       this.username = e.value;
     },
     
     onPasswordChange(e) {
       this.password = e.value;
     },
     
     async onLogin() {
       prompt.showToast({ message: '登录中...' });
       
       try {
         const response = await fetch.fetch({
           url: 'https://api.example.com/api/v1/auth/login',
           method: 'POST',
           data: JSON.stringify({
             username: this.username,
             password: this.password
           })
         });
         
         const data = JSON.parse(response.data);
         if (data.code === 0) {
           router.replace({ uri: '/pages/Index' });
         } else {
           prompt.showToast({ message: data.message });
         }
       } catch (error) {
         prompt.showToast({ message: '登录失败' });
       }
     }
   }
   </script>
   
   <style>
   .container {
     flex-direction: column;
     align-items: center;
     justify-content: center;
     padding: 40px;
   }
   
   input {
     width: 100%;
     height: 80px;
     margin-bottom: 20px;
     border: 1px solid #e5e5e5;
     border-radius: 8px;
     padding: 0 20px;
   }
   </style>
   ```

5. **manifest.json**:
   ```json
   {
     "package": "com.example.app",
     "name": "My App",
     "versionName": "1.0.0",
     "versionCode": 1,
     "minPlatformVersion": 1070,
     "icon": "/common/logo.png",
     "features": [
       { "name": "system.fetch" },
       { "name": "system.router" },
       { "name": "system.prompt" },
       { "name": "system.storage" }
     ],
     "router": {
       "entry": "pages/Index",
       "pages": {
         "pages/Index": {
           "component": "index"
         },
         "pages/Login": {
           "component": "index"
         }
       }
     }
   }
   ```

## Configuration

```yaml
tech_stack:
  quick-app:
    min_platform: 1070
    language: typescript
    ui: custom
```
