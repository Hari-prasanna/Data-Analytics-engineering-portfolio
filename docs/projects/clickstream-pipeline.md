---
title: Clickstream Conversion Pipeline
tags:
  - dbt
  - SQL
  - Airflow
---

# Clickstream Conversion Pipeline

<span class="hp-badge hp-badge--progress" style="font-size: 0.75rem;">In progress</span>

> Real-time conversion funnel analytics from raw clickstream events

## Overview

<!-- TODO: Add your project overview here -->
Describe the conversion funnel problem, what clickstream data looks like, and goals.

## Architecture

```mermaid
flowchart LR
    A[Clickstream<br/>Events] -->|Ingest| B[Raw Events<br/>Store]
    B -->|dbt Models| C[Session<br/>Stitching]
    C --> D[Funnel<br/>Aggregation]
    D --> E[Conversion<br/>Dashboard]

    style A fill:#FAECE7,stroke:#D85A30,color:#712B13
    style B fill:#E6F1FB,stroke:#185FA5,color:#0C447C
    style C fill:#E1F5EE,stroke:#1D9E75,color:#085041
    style D fill:#EEEDFE,stroke:#534AB7,color:#3C3489
    style E fill:#FAEEDA,stroke:#BA7517,color:#854F0B
```

## Tech Decisions

<!-- TODO: Explain your dbt model structure, scheduling strategy, etc. -->

!!! info "Why dbt for transformations?"
    Explain the dbt model layers and testing strategy.

## Code Walkthrough

<!-- TODO: Add key SQL / dbt model snippets -->

```sql
-- Example: funnel staging model
-- Add your actual code here
```

## Current Status

<!-- TODO: What's done, what's left? -->

!!! warning "Work in progress"
    List remaining tasks and next milestones.

---

:octicons-mark-github-16: [View on GitHub](https://github.com/Hari-prasanna/Data-Analytics-engineering-portfolio/tree/main/clickstream-conversion-pipeline){ .md-button }
