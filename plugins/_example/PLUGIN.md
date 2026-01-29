# Example Plugin Template

> This is a template for creating custom plugins for Multi-Platform Transformer.

## Plugin Information

| Field | Value |
|-------|-------|
| Name | example-plugin |
| Version | 1.0.0 |
| Author | Your Name |
| Hooks | on_generate, after_generate |

## Description

Describe what this plugin does and when it should be used.

## Configuration

```yaml
# Add this to your config.yaml under plugins.config
example-plugin:
  option1: value1
  option2: value2
```

## Hook: on_generate

This hook is called during the code generation phase.

### Instructions for AI Agent:

When this hook is triggered:
1. Read the requirement analysis results
2. Apply custom transformation logic
3. Generate additional code or modify existing output

### Input Context:
- `requirements`: Parsed requirement document
- `platform`: Current target platform
- `tech_stack`: Platform tech stack configuration

### Expected Output:
- Additional files to generate
- Modifications to standard output

## Hook: after_generate

This hook is called after all platform code is generated.

### Instructions for AI Agent:

When this hook is triggered:
1. Review generated code for all platforms
2. Apply post-processing logic
3. Generate cross-platform reports or utilities

## Example Usage

```
🤖 "enable example-plugin"
🤖 "generate code with example-plugin"
```

## Files

```
_example/
├── PLUGIN.md           # This file - plugin instructions
├── templates/          # Custom templates
│   └── example.tpl
└── scripts/            # Helper scripts
    └── process.py
```

## Notes

- Keep plugin instructions clear and concise
- Always specify which hooks this plugin uses
- Provide examples for configuration options
