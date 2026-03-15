# Product Performance Dashboard — Spec

## Purpose

Analyse product-level revenue, quantity sold, and category performance. Supports merchandising and inventory decisions.

---

## Data Source

- **Table**: `retail_analytics.marts.mart_product_performance`
- **Refresh**: Daily (post-ETL)

---

## Key Metrics (KPIs)

| Metric | Field | Format | Description |
|--------|-------|--------|-------------|
| Total Revenue (AUD) | `total_revenue_aud` | Currency (AUD) | Sum of line totals |
| Total Quantity Sold | `total_quantity_sold` | Integer | Units sold |
| Product Count | Count of `product_id` | Integer | Distinct products |
| Avg Unit Price (AUD) | `avg_unit_price_aud` | Currency (AUD) | Mean selling price |

---

## Visualisations

### 1. KPI Cards (Top)

- Total Revenue (AUD) — sum
- Total Quantity Sold — sum
- Product Count — distinct count

### 2. Bar Chart — Top 10 Products by Revenue

- **X-axis**: `product_name`
- **Y-axis**: `total_revenue_aud`
- **Sort**: Descending
- **Limit**: 10

### 3. Pie/Donut Chart — Revenue by Category

- **Segment**: `category`
- **Value**: `total_revenue_aud`

### 4. Table — Product Detail

| Column | Type |
|--------|------|
| product_id | String |
| product_name | String |
| category | String |
| order_count | Integer |
| total_quantity_sold | Integer |
| total_revenue_aud | Currency |
| avg_unit_price_aud | Currency |

---

## Filters

- **Category**: Multi-select (Electronics, Apparel, Home, etc.)
- **Product**: Search/filter by `product_name`

---

## Layout

- Row 1: KPI cards (3 columns)
- Row 2: Bar chart (left) | Pie chart (right)
- Row 3: Table (full width)
