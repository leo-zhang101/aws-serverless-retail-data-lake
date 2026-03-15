# Dashboard Screenshots

Place the following 3 screenshots in this folder after running Athena queries or building QuickSight dashboards:

| Filename | Source | Description |
|----------|--------|-------------|
| `daily_sales_dashboard.png` | Athena or QuickSight | Daily sales by store_state: sale_date, order_count, total_sales_aud, avg_order_value_aud |
| `product_performance_dashboard.png` | Athena or QuickSight | Product performance: product_id, product_name, category, total_revenue_aud, total_quantity_sold |
| `customer_value_dashboard.png` | Athena or QuickSight | Customer value: customer_id, customer_name, state, total_spend_aud, total_orders |

**Athena**: Run `sql/athena/sample_analytics_queries.sql` and capture the result grid.

**QuickSight**: Build dashboards per `dashboards/daily_sales_dashboard.md`, `product_performance_dashboard.md`, `customer_value_dashboard.md`.
