---
title: CI/CD Pipelines
tags:
  - GitHub Actions
  - YAML
  - DevOps
---

# CI/CD Pipelines

<span class="hp-badge hp-badge--active" style="font-size: 0.75rem;">Active</span>

> GitHub Actions workflows with path filters for multi-project repo

## Overview

<!-- TODO: Describe your CI/CD strategy -->
Explain how you handle CI/CD across a monorepo with multiple data engineering projects.

## Architecture

```mermaid
flowchart LR
    A[Git Push] --> B{Path Filter}
    B -->|TMDB-ELT/**| C[TMDB Tests<br/>& Deploy]
    B -->|clickstream/**| D[Clickstream<br/>Tests & Deploy]
    B -->|orchestration/**| E[DAG<br/>Validation]

    style A fill:#FAECE7,stroke:#D85A30,color:#712B13
    style B fill:#EEEDFE,stroke:#534AB7,color:#3C3489
    style C fill:#E6F1FB,stroke:#185FA5,color:#0C447C
    style D fill:#E6F1FB,stroke:#185FA5,color:#0C447C
    style E fill:#E1F5EE,stroke:#1D9E75,color:#085041
```

## Workflow Examples

<!-- TODO: Add your actual workflow YAML -->

```yaml
# Example: path-filtered workflow
name: TMDB Pipeline CI
on:
  push:
    paths:
      - 'TMDB-ELT/**'
  pull_request:
    paths:
      - 'TMDB-ELT/**'
```

## Lessons Learned

<!-- TODO: What patterns worked well for monorepo CI/CD? -->

---

:octicons-mark-github-16: [View on GitHub](https://github.com/Hari-prasanna/Data-Analytics-engineering-portfolio/tree/main/.github/workflows){ .md-button }
