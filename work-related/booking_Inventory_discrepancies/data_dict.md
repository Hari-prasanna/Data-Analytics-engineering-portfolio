# Data Dictionary: `HISTORIE_V` (History View)

This table defines the core columns and business logic used across our Internal Transport KPIs and Overstock Inventory Reconciliation queries.

---

## Core Identification & Tracking

| Column Name | Description & Business Context | Example Values / Key Usage |
| :--- | :--- | :--- |
| **`TRANSPORTLHMNR`** / **`LHMNR`** | **Load Carrier Number (Ladehilfsmittelnummer):** The unique physical identifier (barcode/RFID) of the pallet, box, or container being moved. In the Overstock query, `LHMNR` from t1 becomes `Source_LHM` and from t2 becomes `ZIEL_LHM`. Filtering `NOT LIKE '000%'` excludes placeholder carriers. | `100456789`, `50012345` |
| **`LOCAL_TRANSACTION_ID`** | **Transaction Lifecycle Key:** A unique ID linking the start and end of a single inventory movement. The Overstock query self-joins t1 and t2 on this column to stitch "booking out" and "booking in" events into one reconciled record. | `TXN_00129874` |
| **`ZUG_ID`** | **Transport Lifecycle ID:** A unique grouping ID linking all events of a single transport attempt. Used in KPI queries to ensure a completion status (`47`) belongs to the current attempt, not a stale one. | `ZUG_88712` |
| **`ZUGGRUPPE_TOKEN`** | **Group Token:** A unique text string binding multiple transport tasks under a single active order. `COUNT(DISTINCT)` on this accurately calculates "Active Orders" without duplication. | `TOK_A1B2C3` |

## Event Classification

| Column Name | Description & Business Context | Example Values / Key Usage |
| :--- | :--- | :--- |
| **`TYP_ID`** | **Event Type ID:** Numeric code representing the specific status or event logged. *Crucial for KPI logic.* | `42` = Active/Started · `47` = Completed · `39` or `5` = Blocked/Error · `132` = Order Status |
| **`TPARTNR`** | **Transaction Partner Number:** Identifies the type of goods movement being recorded. The Overstock query uses this to split Normal Goods from Dummy Goods across separate CTEs. | `520` = Normal Goods (out/in) · `614` = Dummy Goods (out) · `207` = Dummy Goods (in) |
| **`MENGE`** | **Quantity:** The number of items in the transaction. A negative value (`< 0`) indicates items leaving a location (booking out); a positive value (`= 1`) indicates arrival (booking in). The final output uses `ABS(MENGE)` for clean reporting. | `-1` (out), `1` (in) |

## Location & Routing

| Column Name | Description & Business Context | Example Values / Key Usage |
| :--- | :--- | :--- |
| **`LAGBEZ`** | **Storage Area (Lagerbezeichnung):** The physical zone or storage type. Used to filter source locations in both KPI queries (`AKL`, `Wareneingang`) and Overstock queries (`Overstock`, `SZROV`). | `Overstock` · `SZROV` · `BGL` · `AKL` · `Wareneingang` |
| **`ZIEL`** | **Destination Code:** The target drop-off point for an inventory movement. The Overstock query filters on `LIKE 'OV%'` to isolate Overstock-bound transactions. | `OV01`, `OV02` |
| **`TRANSPORTTASKQUELLE`** | **Transport Source:** Starting location or department where the transport task originated. Used in KPI queries. | `WE` (Wareneingang) · `FIN_AP01` · `BGL` |
| **`TRANSPORTREQUESTZIEL`** / **`TRANSPORTTASKZIEL`** | **Transport Destination:** Target zone or endpoint where the LHM is supposed to be delivered. Used in KPI queries. | `BSF_O` · `FIN_AP` |

## Item & Order Data

| Column Name | Description & Business Context | Example Values / Key Usage |
| :--- | :--- | :--- |
| **`ARTNR`** | **Article Number / EAN:** The item barcode. For Dummy Goods where `ARTNR` doesn't start with `2`, the query falls back to `LASTEANGOTFROMMAUS_ZIEL` from `CUST_DATA` JSON to resolve the actual EAN. | `2001234567890` |
| **`HOSTAUFTRNR`** | **Host Order Number (Auftragsnummer):** The overarching order number from the parent ERP/WMS. `COUNT(DISTINCT)` on this shows unique active *orders* rather than individual pallets. | `ORD-2026-9912` |
| **`ZUGGRUPPE_SENDER`** | **Group Sender/Trigger:** Identifies the internal system process or department that triggered the transport group. | `BESTANDFREIGABE` (Inventory Release) |

## Timestamps & Users

| Column Name | Description & Business Context | Example Values / Key Usage |
| :--- | :--- | :--- |
| **`CREATED`** | **Creation Timestamp:** The exact date and time the system recorded the event. KPI queries filter on rolling windows (`SYSDATE - 5`). The Overstock query filters via parameterized bind variables (`:start_datetime`, `:end_datetime`) using `TO_DATE` with format `DD.MM.YYYY HH24:MI:SS`. | `2026-03-20 14:30:00` |
| **`CREATEDBY`** | **User / Operator:** The system user or warehouse employee who initiated the transaction. Mapped to `BENUTZER` in the Overstock query output. | `USR_SCHMIDT` |

## Semi-Structured Data (JSON)

| Column Name | Description & Business Context | Example Values / Key Usage |
| :--- | :--- | :--- |
| **`CUST_DATA`** | **Custom Data (JSON CLOB):** A JSON blob containing item-level metadata not available in standard columns. The Overstock query extracts multiple fields via `JSON_VALUE`: | `{"SKU_ART": "ZL-1234", ...}` |

### `CUST_DATA` — Extracted JSON Fields

| JSON Path | Output Column | Description | Decode Logic |
| :--- | :--- | :--- | :--- |
| `$.REFERENCENUMBER_LHM` | `Reference_LHM` | Reference carrier number, used as a parameterized filter | Direct extraction |
| `$.QUALITYID_SEKTOR` | `Quality` | Quality grade of the item at sector level | `1` = A · `2` = B · `3` = C · `4` = D |
| `$.QUALITYID_ART` | `Quality` (Dummy fallback) | Quality grade at article level, used via `COALESCE` with `QUALITYID_SEKTOR` for Dummy Goods | Same as above |
| `$.SORTABLE_ART` | `Quality` (override) | Sortability flag. When `false` with `QualityID = 1`: Normal Goods map to `A -> B`, Dummy Goods map to `B` | `true` / `false` |
| `$.SKU_ART` | `SKU` | Stock Keeping Unit. Extracted from t1 for Normal Goods, t2 for Dummy Goods | Direct extraction |
| `$.SORTINGCRITERIAID_ART` | `SORT_ID` | Sorting criteria identifier. Same t1/t2 logic as SKU | Direct extraction |
| `$.CATEGORYID_ART` | `Category` | Product category | `1` = Schuhe · `2` = Textil · `3` = ACC · `4` = Home · `5` = Beauty |
| `$.SOURCEID_SEKTOR` | `Source_Channel` | Origin channel of the item | `1` = Zalando SE · `10` = OSR · `11` = OSR (OV) |
| `$.DISTRIBUTIONCHANNELID_ART` | `Distribution_Channel` | Sales/distribution routing | `3` = Overstock · `4` = Outlet |
| `$.LASTEANGOTFROMMAUS_ZIEL` | `EAN` (fallback) | Actual EAN for Dummy items where `ARTNR` doesn't start with `2` | Direct extraction |