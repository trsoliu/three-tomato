# Baidu Smart Mini Program Generator Plugin

> Generate Baidu Smart Mini Program code from requirement documents.

## Plugin Information

| Field | Value |
|-------|-------|
| Name | baidu-mp-generator |
| Version | 1.0.0 |
| Platform | 百度智能小程序 |
| Hooks | on_generate |

## Supported Tech Stacks

| Category | Options | Default |
|----------|---------|---------|
| Framework | Native, Taro, Uni-app | Native |
| Language | TypeScript, JavaScript | TypeScript |
| UI | Swan UI, Custom | Swan UI |

## Hook: on_generate

### Instructions for AI Agent:

When generating Baidu Smart Mini Program code:

1. **Read Configuration**
   - Check `tech_stack.baidu-mp` in config.yaml

2. **Project Structure**
   ```
   baidu-mp/
   ├── pages/
   │   ├── index/
   │   │   ├── index.swan
   │   │   ├── index.css
   │   │   ├── index.ts
   │   │   └── index.json
   │   └── login/
   ├── components/
   ├── services/
   ├── models/
   ├── utils/
   ├── app.ts
   ├── app.json
   ├── app.css
   ├── project.swan.json
   └── tsconfig.json
   ```

3. **Key Differences**
   - Use `swan` instead of `wx` for APIs
   - Use `.swan` instead of `.wxml`
   - Different component attributes
   - Support for smart components

4. **Code Example**:
   ```typescript
   // pages/login/login.ts
   Page({
     data: {
       username: '',
       password: '',
     },
     
     onUsernameInput(e: { detail: { value: string } }) {
       this.setData({ username: e.detail.value });
     },
     
     async onLogin() {
       swan.showLoading({ title: '登录中...' });
       try {
         // API call
         swan.switchTab({ url: '/pages/index/index' });
       } catch (error) {
         swan.showToast({ title: '登录失败' });
       } finally {
         swan.hideLoading();
       }
     }
   });
   ```

   ```html
   <!-- pages/login/login.swan -->
   <view class="container">
     <input placeholder="用户名" bindinput="onUsernameInput" />
     <button bindtap="onLogin">登录</button>
   </view>
   ```

## Configuration

```yaml
tech_stack:
  baidu-mp:
    framework: native
    language: typescript
    ui: swan-ui
```
