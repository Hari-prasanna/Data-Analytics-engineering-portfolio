---
title: Orchestration Framework
tags:
  - Airflow
  - Docker
  - Astro CLI
---

# Orchestration Framework

<span class="hp-badge hp-badge--infra" style="font-size: 0.75rem;">Infra</span>

> Centralized pipeline orchestration with Astro CLI methods

## Overview

<!-- TODO: Add your project overview here -->
Describe why you built a centralized orchestration layer and how it ties your projects together.

## Architecture

```mermaid
flowchart TD
    A[Astro CLI] --> B[Airflow<br/>Scheduler]
    B --> C[TMDB ELT<br/>DAG]
    B --> D[Clickstream<br/>DAG]
    B --> E[Oracle ETL<br/>DAG]
    C & D & E --> F[Monitoring /<br/>Alerts]

    style A fill:#FAECE7,stroke:#D85A30,color:#712B13
    style B fill:#EEEDFE,stroke:#534AB7,color:#3C3489
    style C fill:#E6F1FB,stroke:#185FA5,color:#0C447C
    style D fill:#E6F1FB,stroke:#185FA5,color:#0C447C
    style E fill:#E6F1FB,stroke:#185FA5,color:#0C447C
    style F fill:#E1F5EE,stroke:#1D9E75,color:#085041
```

## Tech Decisions

!!! info "Why Astro CLI?"
    Explain your choice of Astronomer's CLI for local Airflow development and deployment.

## Setup Guide

<!-- TODO: Add setup steps -->

```bash
# Example: getting started
astro dev init
astro dev start
```

## Lessons Learned

<!-- TODO: What did you learn about orchestration at scale? -->

---

:octicons-mark-github-16: [View on GitHub](https://github.com/Hari-prasanna/Data-Analytics-engineering-portfolio/tree/main/orchestration){ .md-button }
