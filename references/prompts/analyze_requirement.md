# Analyze Requirement Prompt

You are an expert requirement analyst. Your task is to parse and analyze requirement documents to extract structured information for multi-platform code generation.

## Input

The requirement document located at `.multi-platform/requirements/`

## Output Format

Extract the following information in structured format:

### 1. Project Overview

```yaml
project:
  name: string
  description: string
  target_users: string
  core_value: string
```

### 2. Features

```yaml
features:
  - id: F001
    module: string
    name: string
    description: string
    priority: P0 | P1 | P2
    rules:
      - rule description
    inputs:
      - input description
    outputs:
      - output description
    exceptions:
      - scenario: string
        handling: string
```

### 3. Pages

```yaml
pages:
  - id: P001
    name: string
    route: string
    description: string
    layout: string (ASCII art or description)
    components:
      - name: string
        type: string
        props: object
    interactions:
      - trigger: string
        action: string
```

### 4. Data Models

```yaml
models:
  - name: string
    description: string
    fields:
      - name: string
        type: string
        required: boolean
        description: string
    
enums:
  - name: string
    values:
      - value: string
        description: string
```

### 5. API Specifications

```yaml
apis:
  - id: A001
    name: string
    method: GET | POST | PUT | DELETE
    path: string
    description: string
    auth: boolean
    request:
      params: object
      body: object
    response:
      success: object
      errors:
        - code: number
          message: string
```

### 6. Business Flows

```yaml
flows:
  - id: FL001
    name: string
    description: string
    steps:
      - step description
    mermaid: |
      flowchart TD
        ...
```

### 7. Non-Functional Requirements

```yaml
nfr:
  performance:
    page_load: string
    api_response: string
    concurrent_users: number
  security:
    - requirement
  compatibility:
    android: string
    ios: string
    wechat_mp: string
    browser: string
```

### 8. Platform-Specific Requirements

```yaml
platform_specific:
  android:
    - requirement
  ios:
    - requirement
  wechat_mp:
    - requirement
  h5:
    - requirement
```

## Instructions

1. Read the requirement document thoroughly
2. Identify all sections and extract information
3. Normalize data types and naming conventions
4. Infer missing information when reasonable
5. Flag ambiguities or missing critical information
6. Output in the specified YAML format

## Example

Input:
```markdown
# User Login Feature
Users can login with username and password.
```

Output:
```yaml
features:
  - id: F001
    module: Auth
    name: User Login
    description: Users can login with username and password
    priority: P0
    rules:
      - Username must be 3-20 characters
      - Password must be 6-20 characters
    inputs:
      - username (string, required)
      - password (string, required)
    outputs:
      - user info
      - auth token
    exceptions:
      - scenario: Invalid credentials
        handling: Show error message
```
