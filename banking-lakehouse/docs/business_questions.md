# Fraud Detection Project — Stakeholder Questions & Solutions

## Stakeholder Matrix

| # | Stakeholder | The Question | How You Solved It |
|---|---|---|---|
| 1 | **Compliance Officer** *(The Audit Question)* | Did we allow any high-risk customers to move massive amounts of money (>$10k) **exactly while** their internal profile was flagged as "High Risk"? | Built the **SCD Type 2 Dimension** and **Time-Travel Fact Join**. Standard tables would overwrite customer history — SCD2 preserves the exact risk state at the moment of each transaction, so auditors can reconstruct the truth. |
| 2 | **Fraud Operations Team** *(The Tactical Question)* | Which specific transactions from today look highly suspicious so a human analyst can call the customer right now and freeze the funds? | Calculated custom ML features (e.g. `sender_balance_error`, `is_zero_impact_txn`) to surface anomalous behavior, and building the **Google Sheets Reverse ETL** to push actionable transaction IDs straight into the fraud team's daily queue. |
| 3 | **Executive / VP of Risk** *(The Strategic Question)* | What are our overall fraud trends? Are we seeing spikes in "Cash Out" vs. "Transfer" fraud? Are our automated systems flagging correctly? | Built `mart_fraud_dashboard` (the **One Big Table**). Pre-joining all complex data into a flat, wide table lets Metabase instantly load aggregate charts and KPIs without crashing. |

---

## To-Do List

### Compliance Layer (SCD2 + Time-Travel)
- [ ] Validate SCD Type 2 dimension captures `effective_from` / `effective_to` correctly
- [ ] Test time-travel fact join on edge cases (same-day risk flag flips)
- [ ] Write audit query: high-risk customers + transactions > $10k at flagged moment
- [ ] Document the audit query for compliance handoff

### 📋 Cross-Cutting
- [ ] Add data quality tests (dbt tests / Great Expectations) on all three layers
- [ ] Set up alerting for pipeline failures
