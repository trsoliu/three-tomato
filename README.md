<p align="center">
  <img src="./assets/images/three-tomato-logo-color.svg" alt="Three-Tomato Logo" width="200">
</p>

<p align="center">
  <a href="https://skills.sh"><img src="https://img.shields.io/badge/SKILLS.SH-COMPATIBLE-007EC6?style=flat-square" alt="Skills.sh Compatible"></a>
  <img src="https://img.shields.io/badge/VERSION-1.0.0-00B2A9?style=flat-square" alt="Version 1.0.0">
  <a href="LICENSE"><img src="https://img.shields.io/badge/LICENSE-MIT-4c1?style=flat-square" alt="License MIT"></a>
  <a href="https://github.com/trsoliu/three-tomato"><img src="https://img.shields.io/github/stars/trsoliu/three-tomato?style=flat-square&label=STARS&color=EAC54F" alt="Stars"></a>
</p>

# Three-Tomato 三个番茄

> 将需求文档转换为多端原生开发代码：Android、iOS、鸿蒙、小程序、快应用、H5、Web、Mac、Windows 🚀

[📖 中文文档](README.zh.md) · [🐛 报告问题](https://github.com/trsoliu/three-tomato/issues) · [✨ 功能建议](https://github.com/trsoliu/three-tomato/issues)

## ✨ 什么是 Three-Tomato?

Three-Tomato 是一个与 [skills.sh](https://skills.sh) 兼容的技能包，让 AI Agent 能够分析需求文档，并为多个平台生成**原生**开发代码。

**核心理念**：原生优先，AI 友好技术栈（数据集大、文档丰富）

### 💡 使用前

```
📝 PRD 需求文档
     ↓
👨‍💻 Android 开发 → Android 代码
👨‍💻 iOS 开发 → iOS 代码  
👨‍💻 小程序开发 → 小程序代码
👨‍💻 H5/Web 开发 → H5/Web 代码
👨‍💻 桌面端开发 → Mac/Windows 代码
     ↓
🔄 手动同步数据模型、API、业务逻辑...
😰 不一致、Bug、延期...
```

### 🎉 使用后

```
📝 PRD 需求文档
     ↓
🤖 AI Agent + Three-Tomato
     ↓
✅ Android (Kotlin + Compose)
✅ iOS (Swift + SwiftUI)
✅ HarmonyOS (ArkTS + ArkUI)
✅ 微信小程序 (TypeScript 原生)
✅ 支付宝小程序 (TypeScript 原生)
✅ 百度智能小程序 (TypeScript 原生)
✅ 快应用 (TypeScript)
✅ H5 移动端 (React + TypeScript)
✅ Web 桌面端 (Next.js + React)
✅ macOS (Swift + SwiftUI)
✅ Windows (C# + WinUI 3)
     ↓
🎯 一致的数据模型、API、业务逻辑！
```

## 🚀 快速开始

### 安装

```bash
# Using npx
npx skills add trsoliu/three-tomato

# Or clone directly
git clone https://github.com/trsoliu/three-tomato.git
```

### 使用

告诉你的 AI Agent：

```
🤖 "生成多端代码"
🤖 "转换为 Android 代码"
🤖 "transform to ios"
🤖 "生成 Windows 桌面应用"
```

### 更新

```bash
npx skills update trsoliu/three-tomato
```

## 📱 支持的平台（17个）

### 原生平台（11个）

| 平台 | 代码 | 技术栈 |
|------|------|--------|
| **Android** | `android` | Kotlin + Jetpack Compose |
| **iOS** | `ios` | Swift + SwiftUI |
| **HarmonyOS** | `harmony` | ArkTS + ArkUI |
| **微信小程序** | `wechat-mp` | TypeScript 原生 |
| **支付宝小程序** | `alipay-mp` | TypeScript 原生 |
| **百度小程序** | `baidu-mp` | TypeScript 原生 |
| **快应用** | `quick-app` | TypeScript |
| **H5 移动端** | `h5` | React + TypeScript |
| **Web 桌面端** | `web` | Next.js + React |
| **macOS** | `macos` | Swift + SwiftUI |
| **Windows** | `windows` | C# + WinUI 3 |

### 跨端框架（6个）

| 平台 | 代码 | 技术栈 |
|------|------|--------|
| **Flutter** | `flutter` | Dart + Riverpod |
| **React Native** | `react-native` | TypeScript + Zustand |
| **Uni-app** | `uni-app` | Vue 3 + TypeScript |
| **Taro** | `taro` | React + TypeScript |
| **Electron** | `electron` | React + TypeScript |
| **Tauri** | `tauri` | Rust + React |

## 🔌 Plugin System

### Plugin Commands

```
📋 "list plugins"
📦 "install plugin <source>"
✅ "enable plugin <name>"
❌ "disable plugin <name>"
```

### 内置插件

**原生平台生成器（11个）：**
- `android-generator` - Android (Kotlin + Compose)
- `ios-generator` - iOS (Swift + SwiftUI)
- `harmony-generator` - HarmonyOS (ArkTS + ArkUI)
- `wechat-mp-generator` - 微信小程序 (TypeScript)
- `alipay-mp-generator` - 支付宝小程序 (TypeScript)
- `baidu-mp-generator` - 百度智能小程序 (TypeScript)
- `quick-app-generator` - 快应用 (TypeScript)
- `h5-generator` - H5 移动端 (React + TS)
- `web-generator` - Web 桌面端 (Next.js + React)
- `macos-generator` - macOS (Swift + SwiftUI)
- `windows-generator` - Windows (C# + WinUI 3)

**跨端框架生成器（6个）：**
- `flutter-generator` - Flutter (Dart + Riverpod)
- `rn-generator` - React Native (TypeScript + Zustand)
- `uni-app-generator` - Uni-app (Vue 3 + TypeScript)
- `taro-generator` - Taro (React + TypeScript)
- `electron-generator` - Electron 桌面 (React + TypeScript)
- `tauri-generator` - Tauri 桌面 (Rust + React)

**工具类插件：**
- `api-sync` - 跨平台 API 定义同步
- `ui-converter` - UI 组件转换
- `i18n-sync` - 国际化资源同步
- `diff-report` - 平台差异报告

## 📁 输出结构

```
.three-tomato/
├── config.yaml              # 配置文件
├── requirements/            # 需求文档
│   ├── PRD.md
│   └── api.yaml
├── output/                  # 生成的代码
│   ├── android/            # Kotlin + Compose
│   ├── ios/                # Swift + SwiftUI
│   ├── harmony/            # ArkTS + ArkUI
│   ├── wechat-mp/          # TypeScript 原生
│   ├── h5/                 # React + TypeScript
│   ├── web/                # Next.js + React
│   ├── macos/              # Swift + SwiftUI
│   ├── windows/            # C# + WinUI 3
│   └── _shared/            # 共享资源
├── reports/                 # 分析报告
└── cache/                   # 增量缓存
```

## 🏗️ Skill 结构

```
three-tomato/
├── SKILL.md                 # 主指令文件
├── three-tomato.skill       # Skill 清单
├── assets/                  # 配置模板
├── docs/                    # 文档
├── plugins/                 # 插件目录
│   ├── _registry.yaml
│   ├── android-generator/
│   ├── ios-generator/
│   ├── web-generator/
│   ├── macos-generator/
│   ├── windows-generator/
│   └── ...
├── references/              # 提示词和模板
└── scripts/                 # Python 工具
```

## ⚙️ 配置

编辑 `.three-tomato/config.yaml`:

```yaml
platforms:
  enabled:
    - android
    - ios
    - wechat-mp
    - h5
    - web

# AI 友好技术栈（原生优先）
tech_stack:
  android:
    language: kotlin
    ui: compose
    
  ios:
    language: swift
    ui: swiftui
    
  h5:
    framework: react      # React 优先，数据集大
    ui: antd-mobile
    
  web:
    framework: react
    meta_framework: nextjs
    
  windows:
    language: csharp
    ui: winui3

output:
  include_tests: true
  include_docs: true
  language: zh-CN
```

## ❓ 常见问题

**Q: 更新 skill 会影响已生成的代码吗？**

不会。更新只更新 skill 本身，不会修改已生成的代码。使用 `"重新生成代码"` 来更新代码。

**Q: 可以自定义生成的代码吗？**

可以。使用 `<!-- user-content -->` 标记的内容会在重新生成时保留。

**Q: 为什么不支持 Flutter/RN 等跨端框架？**

本项目专注于**原生开发**，原因：
1. 原生性能更好
2. 各平台有独立的开发者和团队
3. 原生技术 AI 数据集更大，生成质量更高

## 🙏 灵感来源

- [mini-wiki](https://github.com/trsoliu/mini-wiki)
- [DeepWiki](https://github.com/AsyncFuncAI/deepwiki-open)

## 📄 许可证

本项目使用 [MIT 许可证](LICENSE)。

## 💬 联系方式

Made with ❤️ by trsoliu

微信: trsoliu
