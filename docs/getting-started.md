# 快速开始 / Getting Started

## 安装 / Installation

### 方式一：使用 npx（推荐）

```bash
npx skills add trsoliu/multi-platform-transformer
```

### 方式二：手动下载

从 [Releases](https://github.com/trsoliu/multi-platform-transformer/releases) 下载 `multi-platform-transformer.skill` 文件，放置到你的 skills 目录。

### 方式三：Git Clone

```bash
git clone https://github.com/trsoliu/multi-platform-transformer.git
```

## 初始化项目 / Initialize Project

在你的项目根目录下，告诉 AI Agent：

```
🤖 "初始化多端转换"
🤖 "init multi-platform transformer"
```

这将创建以下目录结构：

```
.multi-platform/
├── config.yaml         # 配置文件
├── requirements/       # 放置需求文档
├── output/            # 生成的代码
├── cache/             # 缓存目录
└── reports/           # 分析报告
```

## 配置 / Configuration

编辑 `.multi-platform/config.yaml`：

```yaml
# 项目信息
project:
  name: "my-app"
  version: "1.0.0"

# 启用的目标平台
platforms:
  enabled:
    - android      # 原生 Android
    - ios          # 原生 iOS
    - wechat-mp    # 微信小程序
    - h5           # H5/Web

# 技术栈配置
tech_stack:
  android:
    language: kotlin
    architecture: mvvm
    ui: compose
    
  ios:
    language: swift
    architecture: mvvm
    ui: swiftui
    
  wechat-mp:
    framework: native
    language: typescript
    
  h5:
    framework: vue3
    ui: vant
```

## 添加需求文档 / Add Requirements

将你的需求文档放入 `.multi-platform/requirements/` 目录：

```
requirements/
├── PRD.md           # 产品需求文档
├── api.yaml         # API 规范（可选）
└── ui-specs/        # UI 设计稿（可选）
```

你可以使用我们提供的需求文档模板：`assets/requirement.template.md`

## 生成代码 / Generate Code

告诉 AI Agent 开始生成：

```
🤖 "生成多端代码"
🤖 "transform to all platforms"
🤖 "generate android code"
🤖 "转换为微信小程序"
```

## 查看输出 / View Output

生成的代码将位于 `.multi-platform/output/`：

```
output/
├── android/         # Android 项目
├── ios/             # iOS 项目
├── wechat-mp/       # 微信小程序项目
├── h5/              # H5 项目
└── _shared/         # 共享资源
```

每个平台目录都包含完整的项目代码和 README 文件。

## 下一步 / Next Steps

- 阅读 [平台指南](platforms/) 了解各平台详细配置
- 查看 [插件系统](plugins.md) 了解如何扩展功能
- 参考 [最佳实践](best-practices.md) 优化你的工作流程
