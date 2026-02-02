# Three-Tomato 进化日志

> 记录 SKILL 的每次自我改进

## 格式说明

每次进化记录包含：
- **日期**: YYYY-MM-DD
- **触发方式**: 手动/自动
- **问题数量**: 本次处理的问题数
- **改进内容**: 具体改进了什么
- **影响平台**: 涉及哪些平台

---

## 进化记录

### 2026-01-30 | iOS SwiftProtobuf 网络层优化

- **触发方式**: 手动 (`3T 总结归纳进化`)
- **问题数量**: 4
- **影响平台**: iOS (Swift)
- **来源项目**: cag3-west

**发现的问题**:
| ID | 问题 | 频率 |
|----|------|------|
| IOS-001 | SwiftProtobuf 过度封装导致类型混乱 | 1 |
| IOS-002 | Codable 与 SwiftProtobuf.Message 协议冲突 | 1 |
| IOS-003 | pbxproj Sources Build Phase 缺少文件 | 1 |
| IOS-004 | Protobuf 属性名与预期不一致 | 1 |

**改进内容**:
1. 更新 `references/patterns/known-issues.yaml` - 添加 4 个 iOS 问题
2. 更新 `references/patterns/best-practices.yaml` - 添加 BP-IOS-002/003
3. 更新 `plugins/ios-generator/PLUGIN.md` - 重写 gRPC 部分，推荐简洁 APIClient 模式

**核心经验**:
> 使用 SwiftProtobuf 时，直接用 `message.jsonUTF8Data()` 编码和 `Message(jsonUTF8Data:)` 解码，
> 不要过度封装，不要混用 Codable 协议。

---

<!-- 新记录添加在这里 -->

