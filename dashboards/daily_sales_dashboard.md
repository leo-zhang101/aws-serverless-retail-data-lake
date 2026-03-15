# Daily Sales Dashboard — Spec

## Purpose

Monitor daily retail sales performance by store state. Supports Australian enterprise retail analytics.

---

## Data Source

- **Table**: `retail_analytics.marts.mart_daily_sales`
- **Refresh**: Daily (post-ETL)

---

## Key Metrics (KPIs)

| Metric | Field | Format | Description |
|--------|-------|--------|-------------|
| Total Sales (AUD) | `total_sales_aud` | Currency (AUD) | Sum of completed order amounts |
| Order Count | `order_count` | Integer | Distinct orders per day/state |
| Customer Count | `customer_count` | Integer | Distinct customers |
| Avg Order Value (AUD) | `avg_order_value_aud` | Currency (AUD) | Mean order value |

---

## Visualisations

### 1. KPI Cards (Top)

- Total Sales (AUD) — period sum
- Order Count — period sum
- Avg Order Value (AUD) — period average

### 2. Line Chart — Daily Sales Trend

- **X-axis**: `sale_date`
- **Y-axis**: `total_sales_aud`
- **Colour**: `store_state`
- **Filter**: Date range (default: last 30 days)

### 3. Bar Chart — Sales by State

- **X-axis**: `store_state`
- **Y-axis**: `total_sales_aud`
- **Sort**: Descending by total_sales_aud

### 4. Table — Daily Detail

| Column | Type |
|--------|------|
| sale_date | Date |
| store_state | String |
| order_count | Integer |
| customer_count | Integer |
| total_sales_aud | Currency |
| avg_order_value_aud | Currency |

---

## Filters

- **Date Range**: `sale_date` (default: last 30 days)
- **Store State**: Multi-select (NSW, VIC, QLD, etc.)

---

## Layout

- Row 1: KPI cards (3 columns)
- Row 2: Line chart (full width)
- Row 3: Bar chart (left) | Table (right)
