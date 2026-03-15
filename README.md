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

## Why This Project

I wanted a single repo that demonstrates:

- Medallion-style data lake (raw / bronze / silver / gold)
- Glue ETL with real PySpark, not just templates
- Athena for ad-hoc querying
- dbt for analytics models
- Terraform for infrastructure

This project uses an Australian retail context (AUD, NSW, VIC, QLD, etc.) because that is the market I am targeting.

## Current Scope

- **Ingestion**: Lambda reads CSV from `sample_data/` and uploads to the S3 raw layer. EventBridge can trigger it daily.
- **ETL**: Three Glue jobs (`raw_to_bronze`, `bronze_to_silver`, `silver_to_gold`).
- **Query**: Athena external tables over the Gold layer. dbt models on top for staging and marts.
- **BI**: Athena result screenshots and dashboard-ready outputs.

## Design Choices

- **load_date as explicit parameter**: lets the same pipeline rerun for a specific date
- **Overwrite instead of append**: simpler and easier to explain in a portfolio project
- **Left joins on store/customer**: keeps records even when some reference data is missing
- **Missing table = skip, not fail**: improves debugging during demo runs
- **Athena over Redshift**: cheaper and easier for a serverless analytics demo
- **dbt on Athena**: keeps analytics SQL versioned and testable

## Limitations

- No orchestration yet with Step Functions or Airflow
- Sample data only, no CDC
- No true incremental processing yet
- dbt profile still configured manually

## Runtime Evidence

This project has already been executed successfully in AWS:

- Lambda uploaded 7 source files into the S3 raw layer
- Glue jobs completed successfully across raw → bronze → silver → gold
- Athena queried partitioned Gold tables successfully


## Example Athena Query

```sql
SELECT *
FROM daily_sales
WHERE load_date = '2024-03-14';
```

### Query Result

![Athena Query](docs/athena_query_result.png)
