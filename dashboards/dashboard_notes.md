# Dashboard Notes

All metrics in AUD. Screenshots go in `dashboards/screenshots/`:
- `daily_sales_dashboard.png` — sale_date, store_state, order_count, total_sales_aud
- `product_performance_dashboard.png` — product_id, product_name, total_revenue_aud
- `customer_value_dashboard.png` — customer_id, customer_name, total_spend_aud

**Athena**: Run `sql/athena/sample_analytics_queries.sql`, capture result grid.  
**QuickSight**: Build per specs in `daily_sales_dashboard.md`, `product_performance_dashboard.md`, `customer_value_dashboard.md`.

---

## Data Sources

| Dashboard | Primary Mart | Secondary |
|-----------|--------------|-----------|
| Daily Sales | `mart_daily_sales` | — |
| Product Performance | `mart_product_performance` | `stg_products` |
| Customer Value | `mart_customer_value` | `stg_customers` |

---

## QuickSight Setup

1. **Create Data Source**: Connect to Athena workgroup `retail-analytics`, database `retail_analytics`
2. **Create Datasets**: Import `marts.mart_daily_sales`, `marts.mart_product_performance`, `marts.mart_customer_value`
3. **SPICE (Optional)**: For faster dashboards, refresh SPICE datasets on a schedule (e.g. daily via EventBridge + Lambda)

---

## Athena / Glue Catalog

- **Database**: `retail_analytics`
- **Schemas**: `staging`, `intermediate`, `marts`
- **Partitioning**: Mart tables are not partitioned; suitable for small-to-medium datasets. For large scale, consider partitioning `mart_daily_sales` by `sale_date`.

---

## Refresh Strategy

| Mart | Refresh | Notes |
|------|---------|-------|
| mart_daily_sales | Daily | After Glue ETL completes |
| mart_product_performance | Daily | Same as above |
| mart_customer_value | Daily | Same as above |

---

## Australian Retail Context

- **Currency**: AUD
- **States**: NSW, VIC, QLD, WA, SA, TAS, ACT, NT
- **Time Zone**: AEST/AEDT (Australia/Sydney) for date-based filters
