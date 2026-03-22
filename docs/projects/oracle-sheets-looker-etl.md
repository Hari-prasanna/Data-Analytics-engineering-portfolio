---
title: Oracle → Sheets → Looker ETL
tags:
  - Oracle
  - Apps Script
  - Looker
  - Google Sheets
---

# Oracle → Sheets → Looker ETL

<span class="hp-badge hp-badge--work" style="font-size: 0.75rem;">Work</span>

> Automated Oracle DB to Google Sheets sync powering Looker dashboards

## Overview

<!-- TODO: Add your project overview — keep work-appropriate, anonymize as needed -->
Describe the business need, data flow, and how this pipeline supports reporting.

## Architecture

```mermaid
flowchart LR
    A[Oracle DB] -->|Scheduled Query| B[Apps Script<br/>Connector]
    B -->|Write| C[Google Sheets<br/>Data Source]
    C -->|Connect| D[Looker<br/>Dashboards]
    D --> E[Stakeholder<br/>Reports]

    style A fill:#FAECE7,stroke:#D85A30,color:#712B13
    style B fill:#E6F1FB,stroke:#185FA5,color:#0C447C
    style C fill:#E1F5EE,stroke:#1D9E75,color:#085041
    style D fill:#FAEEDA,stroke:#BA7517,color:#854F0B
    style E fill:#EEEDFE,stroke:#534AB7,color:#3C3489
```

## Tech Decisions

!!! info "Why Google Sheets as an intermediary?"
    Explain the constraints that led to this architecture and the tradeoffs.

## Key Metrics

<!-- TODO: Add impact metrics -->

- **Data freshness**: How often does it sync?
- **Rows processed**: Scale of data
- **Stakeholders served**: Who uses the dashboards?

## Lessons Learned

<!-- TODO: What would you do differently in a greenfield scenario? -->

---

:octicons-mark-github-16: [View on GitHub](https://github.com/Hari-prasanna/Data-Analytics-engineering-portfolio/tree/main/work-related/oracle-sheets-looker-etl){ .md-button }
