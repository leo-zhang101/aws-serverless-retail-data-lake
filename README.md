# AWS Serverless Retail Data Platform

Serverless retail analytics platform built on AWS using S3, Glue, Athena, Lambda and Terraform.

## Architecture


![Architecture](docs/architecture.png)

## Tech Stack

- AWS S3
- AWS Glue
- AWS Athena
- AWS Lambda
- AWS EventBridge
- Terraform
- Python
- Parquet

## Pipeline Flow

1. Lambda uploads raw CSV files into the S3 raw layer
2. Glue job transforms raw data into Bronze Parquet datasets
3. Glue job cleans and standardizes Bronze data into Silver
4. Glue job builds Gold analytics tables
5. Athena queries Gold tables for analytics

## Gold Analytics Tables

- daily_sales
- product_performance
- customer_value

## Example Query

```sql
SELECT *
FROM daily_sales
WHERE load_date = '2024-03-14';


# serverless-aws-data-platform

Retail analytics pipeline on AWS. Built to practice end-to-end data engineering: ingestion → ETL → query layer → BI.

## Why this project

I wanted a single repo that demonstrates:
- Medallion-style data lake (raw/bronze/silver/gold)
- Glue ETL with real PySpark, not just templates
- Athena for ad-hoc querying
- dbt for analytics models
- Terraform for infra

Australian retail context (AUD, NSW/VIC/QLD etc.) because that's the market I'm targeting.

## Current scope

- **Ingestion**: Lambda reads CSV from `sample_data/`, uploads to S3 raw. EventBridge can trigger daily.
- **ETL**: 3 Glue jobs (raw→bronze→silver→gold). Bronze = Parquet + metadata. Silver = cleaned, deduped. Gold = analytics tables (daily_sales, product_performance, customer_value) + pass-through dims.
- **Query**: Athena external tables over gold. dbt models on top for staging/marts.
- **BI**: QuickSight or Athena result screenshots.

## Design choices

- **load_date as explicit param**: Lets you re-run for a specific date without changing code. Defaults to today.
- **Overwrite, not append**: Simpler for demo. Real pipeline would use upsert or partition append.
- **Left joins on store/customer**: Orders can exist without store_id; we still want them in daily_sales.
- **Missing table = skip, not fail**: If one CSV didn't land, other tables still process. Easier to debug.
- **Athena over Redshift**: Cheaper for small data. No cluster to manage.
- **dbt on Athena**: Versioned SQL, tests. Glue does the heavy lifting; dbt does the modelling.

## Limitations / intentional simplifications

- No orchestration (Step Functions, Airflow). Glue jobs run manually or via EventBridge.
- Sample data only. No CDC, no incremental.
- Single region (ap-southeast-2). No cross-region.
- dbt profile must be configured manually; not in Terraform.

## Run flow

```bash
cd infrastructure/terraform
terraform init && terraform validate && terraform apply

# Lambda (use load_date to match your test data)
aws lambda invoke --function-name $(terraform output -raw lambda_ingestion_name) \
  --payload '{"load_date":"2024-03-14"}' response.json

# Glue (in order)
terraform output glue_job_names
aws glue start-job-run --job-name <raw-to-bronze>
# wait for SUCCEEDED, then bronze-to-silver, then silver-to-gold

# Athena: replace REPLACE_GOLD_BUCKET in create_external_tables.sql, run DDL, MSCK REPAIR, then sample_analytics_queries.sql
```

See [docs/RUN_CHECKLIST.md](docs/RUN_CHECKLIST.md) for the full sequence.

## Tests

```bash
python3 -m unittest discover tests/ -v
```

Lambda handler (mocked S3) and customer_value aggregation logic.

## Docs

- [Architecture](docs/architecture.md)
- [Run Checklist](docs/RUN_CHECKLIST.md)
- [Athena Runbook](docs/athena_runbook.md)
- [Terraform Validation](docs/terraform_validation_checklist.md)
