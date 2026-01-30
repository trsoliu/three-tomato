# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.1] - 2026-01-30

### 📱 iOS Generator Updates
- Updated code generation templates for iOS (Swift + SwiftUI).
- Refined project structure layout for generated iOS projects.
- Better support for dependency management via SPM.

### 🔧 Core Skill Updates
- Updated guide for gRPC usage: Enforced gRPC for native platforms while using HTTP/JSON fallback for Mini Programs/Web.
- Revised `SKILL.md` instructions for clarity.

## [1.0.0] - 2026-01-29

### 🎉 Initial Release

Three-Tomato 首次发布！将需求文档转换为多端原生开发代码。

### ✨ 支持 17 个平台

**原生平台（11个）：**
- Android (Kotlin + Jetpack Compose)
- iOS (Swift + SwiftUI)
- HarmonyOS (ArkTS + ArkUI)
- 微信小程序 (TypeScript)
- 支付宝小程序 (TypeScript)
- 百度小程序 (TypeScript)
- 快应用 (TypeScript)
- H5 移动端 (React + TypeScript)
- Web 桌面端 (Next.js + React)
- macOS (Swift + SwiftUI)
- Windows (C# + WinUI 3)

**跨端框架（6个）：**
- Flutter (Dart + Riverpod)
- React Native (TypeScript + Zustand)
- Uni-app (Vue 3 + TypeScript)
- Taro (React + TypeScript)
- Electron (React + TypeScript)
- Tauri (Rust + React)

### 🔌 插件系统

- 17 个平台生成器插件
- 6 个工具类插件：`api-sync`, `ui-converter`, `i18n-sync`, `diff-report`, `migration-guide`, `test-generator`
- 支持 6 种钩子：`before_analyze`, `after_analyze`, `before_generate`, `on_generate`, `after_generate`, `on_export`
- YAML 插件注册表
- 支持自定义插件安装

### 🛠 技术特性

- AI 友好技术栈（优先大数据集、文档丰富的技术）
- SKILL.md 指令系统
- 增量缓存支持
- 多语言文档（中英文）
- Python 工具脚本
