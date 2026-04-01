---
title: Experience
---

# Experience

## Data Specialist — Zalando Lounge Logistics SE & Co KG

*Mar 2023 – Present · Berlin, Germany*

### Automated Data Pipelines

Engineered an automated data ingestion pipeline using **Databricks** and **AWS** (managing IP whitelisting), reducing daily download and import processing time by **90%** (from 100 minutes to 10 minutes). The pipeline queries Oracle directly via SQLAlchemy, processes data with Pandas, and pushes results to Google Sheets — powering the [DG Monitor Dashboard](projects/oracle-sheets-looker-etl.md) for dangerous goods compliance.

**Stack:** `Databricks` · `Python` · `Pandas` · `SQLAlchemy` · `Google Sheets API` · `Google Chat Cards V2`

---

### Cost Optimization & Real-Time Dashboarding

Architected a [real-time logistics transparency dashboard](projects/internal-transport-kpi-dashboard.md) displayed on warehouse floor TV monitors. Optimized Databricks job clusters (tuning memory, CPU, node configurations, and DBUs) to run continuously for **18 hours/day** while keeping AWS infrastructure costs to **under €70/month** — saving **~€10,000** compared to external vendor proposals.

Built a zero-maintenance KPI engine that auto-discovers `.sql` files — adding a new KPI requires zero code changes. Grafana streams data to monitors via credential-less TV tokens every 5 minutes.

**Stack:** `Databricks` · `SQLAlchemy` · `Grafana` · `Google Sheets API`

---

### Root Cause Analysis & Advanced SQL

Debugged critical discrepancies in inbound inventory reporting by developing complex SQL queries — leveraging multiple CTEs, UNIONs, and JSON data extraction — to accurately map multi-stage item scanning processes. This reduced external ticket volume and associated costs.

**Stack:** `Oracle SQL` · `CTEs` · `JSON Extraction`

---

### Quality Assurance Automation

Developed a custom data input tool using **Google Sheets** and **Google Apps Script** to integrate with a centralized quality feed. Automated defect tracking by utilizing webhooks to push real-time JSON alert cards directly into Team Lead communication spaces for immediate resolution.

**Stack:** `Google Apps Script` · `Google Sheets` · `Webhooks` · `Google Chat API`

---

## Education

### University of Europe for Applied Sciences

*Master of Science*

Statistics and Numerical Methods · Business Development and Control · Project Management and Finance
