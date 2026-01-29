# Alipay Mini Program Generator Plugin

> Generate Alipay Mini Program code from requirement documents.

## Plugin Information

| Field | Value |
|-------|-------|
| Name | alipay-mp-generator |
| Version | 1.0.0 |
| Platform | 支付宝小程序 |
| Hooks | on_generate |

## Supported Tech Stacks

| Category | Options | Default |
|----------|---------|---------|
| Framework | Native, Taro, Uni-app | Native |
| Language | TypeScript, JavaScript | TypeScript |
| UI | Antd Mini, Custom | Antd Mini |

## Hook: on_generate

### Instructions for AI Agent:

When generating Alipay Mini Program code:

1. **Read Configuration**
   - Check `tech_stack.alipay-mp` in config.yaml

2. **Project Structure**
   ```
   alipay-mp/
   ├── pages/
   │   ├── index/
   │   │   ├── index.axml
   │   │   ├── index.acss
   │   │   ├── index.ts
   │   │   └── index.json
   │   └── login/
   ├── components/
   ├── services/
   ├── models/
   ├── utils/
   ├── app.ts
   ├── app.json
   ├── app.acss
   ├── mini.project.json
   └── tsconfig.json
   ```

3. **Key Differences from WeChat**
   - Use `my` instead of `wx` for APIs
   - Use `.axml` instead of `.wxml`
   - Use `.acss` instead of `.wxss`
   - Different lifecycle methods naming
   - Different component properties

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
       my.showLoading({ content: '登录中...' });
       try {
         // API call
         my.switchTab({ url: '/pages/index/index' });
       } catch (error) {
         my.showToast({ content: '登录失败' });
       } finally {
         my.hideLoading();
       }
     }
   });
   ```

   ```xml
   <!-- pages/login/login.axml -->
   <view class="container">
     <input placeholder="用户名" onInput="onUsernameInput" />
     <button onTap="onLogin">登录</button>
   </view>
   ```

## Configuration

```yaml
tech_stack:
  alipay-mp:
    framework: native
    language: typescript
    ui: antd-mini
```
