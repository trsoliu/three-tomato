# 平台指南 / Platform Guides

本目录包含各平台的详细配置和开发指南。

## 支持的平台

### 原生移动端

| 平台 | 代码 | 文档 |
|------|------|------|
| Android | `android` | [android.md](android.md) |
| iOS | `ios` | [ios.md](ios.md) |
| HarmonyOS | `harmony` | [harmony.md](harmony.md) |

### 小程序

| 平台 | 代码 | 文档 |
|------|------|------|
| 微信小程序 | `wechat-mp` | [wechat-mp.md](wechat-mp.md) |
| 支付宝小程序 | `alipay-mp` | [alipay-mp.md](alipay-mp.md) |
| 百度智能小程序 | `baidu-mp` | [baidu-mp.md](baidu-mp.md) |
| 快应用 | `quick-app` | [quick-app.md](quick-app.md) |

### Web

| 平台 | 代码 | 文档 |
|------|------|------|
| H5/Mobile Web | `h5` | [h5.md](h5.md) |

### 跨端框架

| 平台 | 代码 | 文档 |
|------|------|------|
| Flutter | `flutter` | [flutter.md](flutter.md) |
| React Native | `react-native` | [react-native.md](react-native.md) |
| Uni-app | `uni-app` | [uni-app.md](uni-app.md) |
| Taro | `taro` | [taro.md](taro.md) |

## 平台选择建议

### 场景一：需要最佳性能

推荐：`android` + `ios` 原生开发

### 场景二：快速迭代，资源有限

推荐：`flutter` 或 `react-native` 跨端

### 场景三：微信生态为主

推荐：`wechat-mp` + `h5`

### 场景四：多小程序平台

推荐：`uni-app` 或 `taro` 跨端小程序

### 场景五：全平台覆盖

推荐：分阶段开发
1. 第一阶段：`wechat-mp` + `h5`
2. 第二阶段：`android` + `ios`
3. 第三阶段：其他小程序平台

## 技术栈对比

| 特性 | Android | iOS | WeChat MP | H5 |
|------|---------|-----|-----------|-----|
| 语言 | Kotlin/Java | Swift/ObjC | TS/JS | TS/JS |
| UI | Compose/XML | SwiftUI/UIKit | WXML | Vue/React |
| 状态管理 | ViewModel | ObservableObject | MobX/Redux | Pinia/Redux |
| 网络 | Retrofit | Alamofire | wx.request | Axios |
| 存储 | Room | Core Data | Storage | IndexedDB |

## 平台差异处理

### 1. API 差异

不同平台的 API 调用方式不同，但数据模型保持一致：

```typescript
// 统一的 User 模型
interface User {
  id: string;
  username: string;
  avatar?: string;
}
```

### 2. UI 差异

UI 组件名称和用法不同，但布局结构相似：

| 组件 | Android | iOS | WeChat MP | H5 (Vue) |
|------|---------|-----|-----------|----------|
| 容器 | Column | VStack | view | div |
| 文本 | Text | Text | text | span |
| 按钮 | Button | Button | button | button |
| 输入框 | TextField | TextField | input | input |

### 3. 导航差异

| 平台 | 导航方式 |
|------|----------|
| Android | Navigation Compose / Fragment |
| iOS | NavigationStack / UINavigationController |
| WeChat MP | wx.navigateTo / wx.switchTab |
| H5 | Vue Router / React Router |

## 更多资源

- [API 同步指南](../api-sync.md)
- [UI 转换指南](../ui-converter.md)
- [国际化指南](../i18n.md)
