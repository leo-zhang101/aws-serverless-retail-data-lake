# Athena Runbook

## Prerequisites

1. Terraform applied; Glue jobs (raw→bronze→silver→gold) run successfully.
2. Gold S3 bucket has data under `{table}/load_date=YYYY-MM-DD/`.
3. Athena workgroup and result bucket from Terraform outputs.

## Create Tables

1. **Get gold bucket name**:
   ```bash
   terraform -chdir=infrastructure/terraform output gold_bucket
   ```

2. **Edit `sql/athena/create_external_tables.sql`**: Replace all `REPLACE_GOLD_BUCKET` with the actual bucket name.

3. **Create database** (if not exists):
   ```sql
   CREATE DATABASE IF NOT EXISTS retail_analytics;
   ```

4. **Run DDL**: In Athena query editor, execute each `CREATE EXTERNAL TABLE` from the edited file. Or run the full script.

5. **Repair partitions** (discover load_date partitions):
   ```sql
   MSCK REPAIR TABLE daily_sales;
   MSCK REPAIR TABLE product_performance;
   MSCK REPAIR TABLE customer_value;
   MSCK REPAIR TABLE customers;
   MSCK REPAIR TABLE orders;
   MSCK REPAIR TABLE order_items;
   MSCK REPAIR TABLE products;
   MSCK REPAIR TABLE payments;
   MSCK REPAIR TABLE stores;
   MSCK REPAIR TABLE promotions;
   ```

## Select Workgroup

1. In Athena console, use the workgroup dropdown.
2. Choose the workgroup from Terraform output (e.g. `retail-analytics-dev-abc12345`).
3. Result location is `s3://{athena_results_bucket}/athena-results/`.

## Run Analytics SQL

1. Open `sql/athena/sample_analytics_queries.sql`.
2. Ensure tables have partitions (MSCK REPAIR run).
3. Execute queries; the `WHERE load_date = (SELECT MAX(load_date)...)` uses the latest partition.

## Expected Results

| Query | Output |
|-------|--------|
| Daily sales | sale_date, store_state, order_count, total_sales_aud, avg_order_value_aud |
| Product performance | product_id, product_name, category, total_revenue_aud, total_quantity_sold |
| Customer value | customer_id, customer_name, state, total_spend_aud, total_orders |

All monetary values are in **AUD**.
