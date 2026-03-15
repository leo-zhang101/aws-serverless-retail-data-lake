# Customer Value Dashboard — Spec

## Purpose

Understand customer lifetime value, order frequency, and spend distribution. Supports CRM and marketing segmentation.

---

## Data Source

- **Table**: `retail_analytics.marts.mart_customer_value`
- **Refresh**: Daily (post-ETL)

---

## Key Metrics (KPIs)

| Metric | Field | Format | Description |
|--------|-------|--------|-------------|
| Total Customers | Count of `customer_id` | Integer | Distinct customers |
| Total Spend (AUD) | `total_spend_aud` | Currency (AUD) | Sum of completed order amounts |
| Avg Order Value (AUD) | `avg_order_value_aud` | Currency (AUD) | Mean order value per customer |
| Avg Orders per Customer | `total_orders` | Decimal | Mean orders per customer |

---

## Visualisations

### 1. KPI Cards (Top)

- Total Customers — count
- Total Spend (AUD) — sum
- Avg Order Value (AUD) — average

### 2. Bar Chart — Top 10 Customers by Spend

- **X-axis**: `customer_name`
- **Y-axis**: `total_spend_aud`
- **Sort**: Descending
- **Limit**: 10

### 3. Bar Chart — Spend by State

- **X-axis**: `state`
- **Y-axis**: `total_spend_aud`
- **Sort**: Descending

### 4. Table — Customer Detail

| Column | Type |
|--------|------|
| customer_id | Integer |
| customer_name | String |
| state | String |
| first_order_date | Date |
| total_orders | Integer |
| total_spend_aud | Currency |
| avg_order_value_aud | Currency |

---

## Filters

- **State**: Multi-select (NSW, VIC, QLD, etc.)
- **Spend Range**: Min/max `total_spend_aud`
- **Order Count**: Min `total_orders` (e.g. repeat customers)

---

## Layout

- Row 1: KPI cards (3 columns)
- Row 2: Top customers bar (left) | Spend by state bar (right)
- Row 3: Table (full width)
