# Project Structure

Complete folder and file layout for `serverless-aws-data-platform`, with the role of each component.

---

## Root Level

| File | Role |
|------|------|
| `README.md` | Project overview, tech stack, setup instructions, and portfolio value proposition |
| `.env.example` | Template for environment variables (AWS region, bucket names, Glue/Athena config). Copy to `.env` for local use |
| `.gitignore` | Excludes Terraform state, Python cache, dbt artifacts, IDE config, and secrets |
| `PROJECT_STRUCTURE.md` | This file – explains the role of every folder and file |

---

## `docs/`

Documentation for architecture, resume, and interviews.

| File | Role |
|------|------|
| `architecture.md` | End-to-end data flow: S3 zones, Glue ETL pipeline, Athena tables, dbt marts |
| `aws_production_mapping.md` | Mapping of project components to AWS resources |
| `athena_runbook.md` | Athena DDL, MSCK REPAIR, query execution |
| `RUN_CHECKLIST.md` | Execution order: terraform → lambda → glue → athena → dashboards |
| `terraform_validation_checklist.md` | terraform fmt/init/validate/plan/apply steps |
| `resume_bullets.md` | Australian-style resume bullet points |
| `interview_talking_points.md` | Interview Q&A for this project |

---

## `dashboards/`

BI dashboard specifications for QuickSight.

| File | Role |
|------|------|
| `dashboard_notes.md` | BI layer overview, QuickSight setup, refresh strategy |
| `daily_sales_dashboard.md` | Spec for daily sales dashboard (KPIs, charts, filters) |
| `product_performance_dashboard.md` | Spec for product performance dashboard |
| `customer_value_dashboard.md` | Spec for customer value dashboard |

---

## `infrastructure/terraform/`

Terraform modules for AWS resources. All infrastructure is defined here.

| File | Role |
|------|------|
| `main.tf` | Root module, locals, and high-level resource orchestration |
| `variables.tf` | Input variables (project name, region, environment) |
| `outputs.tf` | Outputs (bucket names, Glue DB, Athena workgroup, Lambda ARN) |
| `providers.tf` | AWS provider configuration (region, credentials) |
| `versions.tf` | Terraform and provider version constraints |
| `s3.tf` | S3 buckets: raw, bronze, silver, gold, Athena results |
| `glue.tf` | Glue database and ETL job definitions |
| `iam.tf` | IAM roles and policies for Glue, Lambda, Athena |
| `athena.tf` | Athena workgroup and query result location |
| `lambda.tf` | Lambda function for ingestion (upload/move files to raw S3) |
| `eventbridge.tf` | EventBridge schedule to trigger Lambda ingestion |

---

## `ingestion/lambda/`

Lambda function that simulates or performs data ingestion into the raw S3 zone.

| File | Role |
|------|------|
| `app.py` | Lambda handler: reads sample data, uploads to `s3://raw/...` with `load_date` partitioning |
| `requirements.txt` | Python dependencies (boto3, etc.) for Lambda deployment package |

---

## `glue_jobs/`

AWS Glue ETL scripts (PySpark). Deployed to S3 and referenced by Glue job definitions.

| File | Role |
|------|------|
| `raw_to_bronze.py` | Reads raw CSV from S3, applies basic schema, writes to bronze with `load_date` partition |
| `bronze_to_silver.py` | Cleans bronze data: null handling, deduplication, invalid record filtering. Writes to silver |
| `silver_to_gold.py` | Joins silver tables, builds business-level aggregates. Writes to gold zone |

---

## `sql/athena/`

SQL for Athena: external table DDL and sample analytics queries.

| File | Role |
|------|------|
| `create_external_tables.sql` | DDL for external tables over bronze/silver/gold S3 paths. Partitioned by `load_date` |
| `sample_analytics_queries.sql` | Example queries: daily sales, product performance, customer value (AUD metrics) |

---

## `dbt/retail_analytics/`

dbt project for analytics models. Targets Athena (or compatible warehouse).

| File / Folder | Role |
|---------------|------|
| `dbt_project.yml` | Project config: name, profile, model paths, tests |
| `profiles.yml.example` | Example dbt profile for Athena (region, workgroup, output location) |
| `models/_sources.yml` | Source definitions for gold layer tables |
| `models/staging/` | Staging models: stg_customers, stg_orders, stg_products, stg_payments, stg_stores, stg_promotions, stg_order_items |
| `models/intermediate/` | Intermediate models: int_order_items, int_orders_enriched, int_customer_orders |
| `models/marts/` | Mart models: mart_daily_sales, mart_product_performance, mart_customer_value |
| `macros/` | Reusable SQL macros (e.g. AUD formatting, date helpers) |
| `tests/` | dbt tests: uniqueness, not_null, referential integrity |

---

## `sample_data/`

Sample CSV files for local testing and Lambda ingestion simulation.

| File | Role |
|------|------|
| `customers.csv` | Customer dimension: id, name, email, state (Australian states) |
| `orders.csv` | Order fact: order_id, customer_id, store_id, date, amount (AUD), status, promotion_id |
| `order_items.csv` | Order line items: order_item_id, order_id, product_id, quantity, unit_price (AUD), line_total (AUD) |
| `products.csv` | Product dimension: id, name, category, unit_price (AUD) |
| `payments.csv` | Payment fact: payment_id, order_id, amount (AUD), method, date |
| `stores.csv` | Store dimension: store_id, store_name, state, city, opened_at |
| `promotions.csv` | Promotion dimension: promotion_id, name, discount_type, discount_value_pct, start_date, end_date, active |

---

## Data Flow Summary

```
sample_data/*.csv
       │
       ▼
Lambda (ingestion) ──► s3://raw/.../load_date=YYYY-MM-DD/
       │
       ▼
Glue: raw_to_bronze ──► s3://bronze/.../load_date=YYYY-MM-DD/
       │
       ▼
Glue: bronze_to_silver ──► s3://silver/.../load_date=YYYY-MM-DD/
       │
       ▼
Glue: silver_to_gold ──► s3://gold/.../load_date=YYYY-MM-DD/
       │
       ▼
Athena (external tables) ──► SQL queries
       │
       ▼
dbt (staging + marts) ──► mart_daily_sales, mart_product_performance, mart_customer_value
       │
       ▼
QuickSight (optional BI layer)
```

---

## Naming Conventions

- **S3**: `{project}-{env}-{zone}-{suffix}` (e.g. `retail-analytics-dev-raw-abc12345`)
- **Glue**: `retail_analytics` database, `raw_to_bronze` job names
- **Athena**: `retail_analytics` workgroup
- **dbt**: `stg_*` for staging, `mart_*` for marts
- **Partitioning**: `load_date` (YYYY-MM-DD) across all zones
