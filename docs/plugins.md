# 插件系统 / Plugin System

Multi-Platform Transformer 使用基于指令的插件系统，允许扩展和自定义代码生成行为。

## 插件类型

### 1. 平台生成器插件

负责生成特定平台的代码：

- `android-generator` - Android 原生代码生成
- `ios-generator` - iOS 原生代码生成
- `harmony-generator` - HarmonyOS 代码生成
- `wechat-mp-generator` - 微信小程序代码生成
- `alipay-mp-generator` - 支付宝小程序代码生成
- `baidu-mp-generator` - 百度智能小程序代码生成
- `quick-app-generator` - 快应用代码生成
- `h5-generator` - H5/Web 代码生成
- `flutter-generator` - Flutter 代码生成
- `rn-generator` - React Native 代码生成
- `uni-app-generator` - Uni-app 代码生成
- `taro-generator` - Taro 代码生成

### 2. 工具插件

提供辅助功能：

- `api-sync` - API 定义同步
- `ui-converter` - UI 组件转换
- `i18n-sync` - 国际化资源同步
- `diff-report` - 平台差异报告
- `migration-guide` - 迁移指南生成
- `test-generator` - 测试代码生成
- `doc-generator` - 文档生成

## 插件命令

使用自然语言与 AI Agent 交互：

```
📋 "list plugins"              # 列出所有插件
📋 "list platform plugins"     # 列出平台插件
📦 "install plugin <source>"   # 安装插件
🔄 "update plugin <name>"      # 更新插件
✅ "enable plugin <name>"      # 启用插件
❌ "disable plugin <name>"     # 禁用插件
```

或使用 CLI：

```bash
python scripts/plugin_manager.py list
python scripts/plugin_manager.py install owner/repo
python scripts/plugin_manager.py enable android-generator
python scripts/plugin_manager.py disable test-generator
```

## 插件安装来源

### GitHub

```
📦 "install plugin owner/repo"
📦 "install trsoliu/my-plugin"
```

### URL

```
📦 "install plugin https://example.com/plugin.zip"
```

### 本地路径

```
📦 "install plugin ./my-local-plugin"
```

## Hook 系统

插件通过 Hook 在特定时机执行：

| Hook | 时机 | 用途 |
|------|------|------|
| `before_analyze` | 需求分析前 | 预处理需求文档 |
| `after_analyze` | 需求分析后 | 后处理分析结果 |
| `before_generate` | 代码生成前 | 修改生成参数 |
| `on_generate` | 代码生成时 | 执行代码生成 |
| `after_generate` | 代码生成后 | 后处理生成代码 |
| `on_export` | 导出时 | 生成报告等 |

### Hook 执行顺序

在 `plugins/_registry.yaml` 中定义：

```yaml
hook_order:
  before_analyze:
    - api-sync
  on_generate:
    - android-generator
    - ios-generator
    - wechat-mp-generator
  after_generate:
    - api-sync
    - i18n-sync
  on_export:
    - diff-report
    - doc-generator
```

## 创建自定义插件

### 1. 创建插件目录

```
my-plugin/
├── PLUGIN.md      # 插件指令（必需）
├── templates/     # 模板文件（可选）
└── scripts/       # 辅助脚本（可选）
```

### 2. 编写 PLUGIN.md

```markdown
# My Plugin

## Plugin Information

| Field | Value |
|-------|-------|
| Name | my-plugin |
| Version | 1.0.0 |
| Hooks | on_generate |

## Description

描述插件功能...

## Hook: on_generate

### Instructions for AI Agent:

当此 hook 触发时：
1. 步骤 1
2. 步骤 2
3. 步骤 3

## Configuration

```yaml
plugins:
  config:
    my-plugin:
      option1: value1
```
```

### 3. 注册插件

安装后，插件会自动注册到 `plugins/_registry.yaml`。

## 插件配置

在 `config.yaml` 中配置插件：

```yaml
plugins:
  enabled:
    - android-generator
    - ios-generator
    - api-sync
    
  config:
    api-sync:
      auto_sync: true
      formats:
        - openapi
        - typescript
        
    diff-report:
      format: markdown
      include_code_samples: true
```

## 最佳实践

1. **保持插件单一职责** - 每个插件只做一件事
2. **提供清晰的指令** - PLUGIN.md 中的指令要具体明确
3. **支持配置** - 允许用户自定义行为
4. **处理错误** - 优雅处理异常情况
5. **保持兼容** - 不破坏其他插件的功能
