# Overstock Inventory Reconciliation

![SQL](https://img.shields.io/badge/Language-Oracle_SQL-orange)
![Data Engineering](https://img.shields.io/badge/Focus-Data_Engineering_%26_ETL-blue)
![Impact](https://img.shields.io/badge/Impact-100%25_Accuracy_Restored-green)

## 📋 Executive Summary

This project addresses a critical "data drift" issue in the Overstock department's inventory tracking system. The solution is a complex SQL algorithm that reconciles transaction logs by stitching together disjointed "booking out" and "booking in" events across both Normal and Dummy goods. The query restored **100% accuracy** to inventory reports and was adopted by the TGW team as the standard for stock level validation.

---

## 🧐 The Business Challenge

The Overstock department relied on a legacy report to track inventory movements that suffered from significant data discrepancies:

* **Data Drift:** The legacy system failed to record specific transaction types, creating a growing gap between physical stock and digital records.
* **Black Box Logic:** The root cause was initially unknown, making stock levels untrustworthy for operational planning.
* **Missing "Dummy" Items:** Investigation revealed that the system completely ignored "dummy item" barcodes (temporary placeholders), causing inventory to vanish from the logs.

## 🛠️ The Data Engineering Solution

I reverse-engineered the transaction flow and built a robust SQL solution from scratch. The core logic tracks the **complete lifecycle** of an item — identifying when it leaves a location (`MENGE < 0`) and matching it to its arrival at the destination (`MENGE = 1`) via a self-join on `LOCAL_TRANSACTION_ID`.

### Key Technical Implementations

1. **Complex Logic Decomposition (CTEs):** Four dedicated CTEs separate the transaction lifecycle: `normal_goods_t1` / `t2` for standard items and `dummy_goods_t1` / `t2` for placeholder barcodes, merged via a `combined_transactions` CTE using `UNION ALL`.

2. **Semi-Structured Data Parsing (JSON):** The source system stores critical metadata inside a JSON CLOB column (`CUST_DATA`). The query uses `JSON_VALUE` extensively to extract SKU, Quality Grade, Category, Source Channel, Distribution Channel, and Reference LHM into normalized tabular columns.

3. **Dual-Source Quality Logic:** Quality grading uses a `CASE` expression with a `SORTABLE_ART` override — for Normal Goods, a `QualityID = 1` with `SORTABLE_ART = false` maps to `A -> B`. For Dummy Goods, quality is resolved via `COALESCE` across t2 and t1 records, since the definitive metadata often only exists in the completion transaction.

4. **Flexible Parameterized Filtering:** The query accepts three bind variables (`:start_datetime`, `:end_datetime`, `:ref_lhm_filter`) with built-in support for single values, comma-separated lists, and LIKE wildcards — all handled in a single `WHERE` clause without dynamic SQL.

5. **Business-Readable Normalization:** `DECODE` and `CASE` statements translate internal system codes into human-readable terms — Source Channel (`1` → `Zalando SE`, `10` → `OSR`), Category (`1` → `Schuhe`, `2` → `Textil`), Distribution Channel, and Quality Grades.

6. **Reconciliation Guardrails:** The final `WHERE` clause enforces data integrity — filtering out same-source/destination movements (`Source_LHM ≠ ZIEL_LHM`) and non-numeric destination LHMs via `REGEXP_LIKE`.

---

## 💻 The SQL Logic

### CTE Pipeline

```text
normal_goods_t1  ──┐                    
                   ├── JOIN on LOCAL_TRANSACTION_ID ──┐
normal_goods_t2  ──┘                                 │
                                                     ├── UNION ALL ── combined_transactions ── FINAL SELECT
dummy_goods_t1   ──┐                                 │
                   ├── JOIN on LOCAL_TRANSACTION_ID ──┘
dummy_goods_t2   ──┘
```

### Logic Breakdown

1. **`normal_goods_t1` & `t2`:** Captures standard items (`TPARTNR = 520`) leaving Overstock/SZROV locations (t1, `MENGE < 0`) and their completion records (t2, `MENGE = 1`). SKU and Quality are extracted directly from the t1 record.

2. **`dummy_goods_t1` & `t2`:** Captures dummy items (`TPARTNR = 614` / `207`). **Crucial Logic:** For dummy items, the actual EAN is conditionally extracted — if `ARTNR` doesn't start with `2`, it falls back to `LASTEANGOTFROMMAUS_ZIEL` from JSON. SKU, Quality, and Sort ID are only reliably available from the t2 completion record.

3. **`combined_transactions`:** Merges both streams via `UNION ALL`, applying date range and reference LHM filters. Tags each row with `good_type` (`NORMAL` / `DUMMY`) to drive conditional extraction in the final select.

4. **Final Select:** Applies business-readable formatting, reconciliation guardrails, and outputs the complete inventory movement record with Timestamp, EAN, Quality, Category, Source Channel, Distribution Channel, SKU, and Sort ID.

### Parameters

| Parameter | Format | Description |
| :--- | :--- | :--- |
| `:start_datetime` | `DD.MM.YYYY HH24:MI:SS` | Start of time window |
| `:end_datetime` | `DD.MM.YYYY HH24:MI:SS` | End of time window |
| `:ref_lhm_filter` | `REF123`, `REF123,REF456`, or `REF%` | Single value, comma-separated list, or LIKE wildcard |

---

## 🚀 Impact & Results

* **100% Accuracy Restored:** The new logic captured previously missing "dummy" transactions, eliminating the data drift entirely.
* **Cross-Team Adoption:** The solution was verified and implemented by the TGW (Technical) team as the primary source of truth for Overstock booking.
* **Historical Correction:** The query allowed the business to retroactively correct inventory data from previous periods.
