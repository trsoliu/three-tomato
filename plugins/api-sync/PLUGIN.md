# API Sync Plugin

> Synchronize API definitions and clients across all platforms.

## Plugin Information

| Field | Value |
|-------|-------|
| Name | api-sync |
| Version | 1.0.0 |
| Type | Utility |
| Hooks | after_analyze, after_generate |

## Description

This plugin ensures API interfaces remain consistent across all generated platforms by:
- Parsing OpenAPI/Swagger specifications
- Generating platform-specific API clients
- Maintaining consistent naming conventions
- Synchronizing request/response models

## Hook: after_analyze

### Instructions for AI Agent:

After requirement analysis:
1. Parse API specifications from `requirements/api.yaml` or inline definitions
2. Normalize API endpoints into a common format
3. Store normalized APIs in cache for generators to use

## Hook: after_generate

### Instructions for AI Agent:

After code generation:
1. Verify all platforms have consistent API implementations
2. Check for missing endpoints in any platform
3. Generate API comparison report

## Output

Generates `_shared/api/` directory with:
```
_shared/api/
├── openapi.yaml       # Unified OpenAPI spec
├── endpoints.json     # Normalized endpoints list
├── models.json        # Shared data models
└── README.md          # API documentation
```

## Configuration

```yaml
plugins:
  config:
    api-sync:
      auto_sync: true
      formats:
        - openapi
        - typescript
        - kotlin
        - swift
      validation: strict
```
