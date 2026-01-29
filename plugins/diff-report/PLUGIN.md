# Diff Report Plugin

> Generate platform comparison and difference reports.

## Plugin Information

| Field | Value |
|-------|-------|
| Name | diff-report |
| Version | 1.0.0 |
| Type | Utility |
| Hooks | on_export |

## Description

Generates comprehensive comparison reports showing:
- Feature implementation differences across platforms
- Code structure comparisons
- API implementation variations
- UI component mappings
- Platform-specific limitations

## Hook: on_export

### Instructions for AI Agent:

When generating diff report:

1. **Collect Information**
   - Read all generated platform outputs
   - Extract feature implementations
   - Map components across platforms

2. **Generate Comparison Matrix**
   ```markdown
   | Feature | Android | iOS | WeChat MP | H5 |
   |---------|---------|-----|-----------|-----|
   | Login | ✅ | ✅ | ✅ | ✅ |
   | Biometric Auth | ✅ | ✅ | ❌ | ❌ |
   | Push Notification | ✅ | ✅ | ⚠️ | ❌ |
   ```

3. **Document Differences**
   - Platform-specific implementations
   - Alternative approaches
   - Workarounds for unsupported features

## Output

Generates `reports/comparison.md`:
```markdown
# Platform Comparison Report

## Feature Matrix
...

## Implementation Differences
...

## Platform Limitations
...

## Recommendations
...
```

## Configuration

```yaml
plugins:
  config:
    diff-report:
      format: markdown
      include_code_samples: true
      show_alternatives: true
```
