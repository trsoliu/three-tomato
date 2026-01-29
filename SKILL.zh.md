# Multi-Platform Transformer 技能说明

> 将需求文档转换为多端开发规范和代码

## 概述

此技能让 AI Agent 能够分析需求文档，并为 Android、iOS、鸿蒙、小程序、快应用、H5 等多个平台生成平台特定的开发规范、代码模板和实现指南。

## 支持的平台

| 平台 | 代码 | 描述 |
|------|------|------|
| Android | `android` | 原生 Android (Kotlin/Java) |
| iOS | `ios` | 原生 iOS (Swift/Objective-C) |
| 鸿蒙 | `harmony` | HarmonyOS (ArkTS/ArkUI) |
| 微信小程序 | `wechat-mp` | 微信小程序 |
| 支付宝小程序 | `alipay-mp` | 支付宝小程序 |
| 百度智能小程序 | `baidu-mp` | 百度智能小程序 |
| 快应用 | `quick-app` | 快应用 |
| H5/Web | `h5` | 移动Web (Vue/React) |
| Flutter | `flutter` | 跨平台 Flutter |
| React Native | `react-native` | 跨平台 RN |
| Uni-app | `uni-app` | 跨端统一开发 |
| Taro | `taro` | 多端统一开发 |

## 触发命令

```
🤖 "转换为[平台]"
🤖 "生成[平台]代码"
🤖 "生成多端代码"
🤖 "创建平台规范"
```

## 工作流程

### 阶段1：需求分析
1. 从 `.multi-platform/requirements/` 读取需求文档
2. 解析并提取：
   - 功能规格
   - UI/UX 需求
   - 数据模型
   - API 接口
   - 业务流程

### 阶段2：平台选择
1. 读取 `.multi-platform/config.yaml` 获取目标平台
2. 检查 `plugins/_registry.yaml` 中启用的插件
3. 根据用户命令或配置确定输出平台

### 阶段3：代码生成
对每个目标平台：
1. 从 `references/templates/[platform]/` 加载平台特定模板
2. 应用技术栈配置
3. 生成：
   - 项目结构
   - UI 组件
   - 数据模型
   - API 客户端
   - 业务逻辑
   - 平台特定配置

### 阶段4：输出与验证
1. 将生成的代码写入 `.multi-platform/output/[platform]/`
2. 生成对比矩阵
3. 创建平台间迁移指南

## 配置说明

从 `.multi-platform/config.yaml` 读取配置：

```yaml
# 目标平台
platforms:
  - android
  - ios
  - wechat-mp
  - h5

# 技术栈偏好
tech_stack:
  android:
    language: kotlin
    architecture: mvvm
    di: hilt
    network: retrofit
    
  ios:
    language: swift
    architecture: mvvm
    ui: swiftui
    
  wechat-mp:
    framework: native
    state: mobx
    
  h5:
    framework: vue3
    ui: vant
```

## 重要指令

### 对于 AI Agent：

1. **始终先读取配置**：生成前检查 `.multi-platform/config.yaml`
2. **遵循技术栈**：使用配置的框架和库
3. **保持一致性**：确保数据模型和 API 调用跨平台一致
4. **平台习惯**：遵循各平台的最佳实践和惯例
5. **增量更新**：使用缓存仅重新生成更改的部分
6. **保留用户内容**：`<!-- user-content -->` 标记的内容不得被覆盖

### 代码质量标准：
- 遵循平台特定的编码规范
- 包含适当的错误处理
- 添加必要的注释（使用配置的语言）
- 当 `include_tests: true` 时生成单元测试
- 创建包含设置说明的平台特定 README

## 版本

- 技能版本：1.0.0
- 最后更新：2025-01-29
- 作者：three-tomato
