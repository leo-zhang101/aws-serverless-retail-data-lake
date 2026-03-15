# AWS Production Mapping

Mapping of project components to AWS resources for production deployment.

---

## S3 Buckets

| Logical Name | Terraform Resource | Purpose |
|--------------|--------------------|---------|
| Raw | `aws_s3_bucket.raw` | Incoming CSV files, partitioned by `load_date` |
| Bronze | `aws_s3_bucket.bronze` | Schema-on-read Parquet, raw → bronze output |
| Silver | `aws_s3_bucket.silver` | Cleaned, deduplicated Parquet |
| Gold | `aws_s3_bucket.gold` | Curated business-level tables |
| Athena Results | `aws_s3_bucket.athena_results` | Athena query output location |

**Path Pattern**: `s3://{bucket}/{table}/load_date=YYYY-MM-DD/`

---

## Glue Catalog

| Resource | Terraform | Description |
|----------|-----------|-------------|
| Database | `aws_glue_catalog_database.retail` | `retail_analytics` |
| Crawler (Raw) | `aws_glue_crawler.raw` | Discovers raw CSV schema |
| Crawler (Bronze) | `aws_glue_crawler.bronze` | Discovers bronze Parquet |
| Job: raw_to_bronze | `aws_glue_job.raw_to_bronze` | ETL script from `glue_jobs/raw_to_bronze.py` |
| Job: bronze_to_silver | `aws_glue_job.bronze_to_silver` | ETL script from `glue_jobs/bronze_to_silver.py` |
| Job: silver_to_gold | `aws_glue_job.silver_to_gold` | ETL script from `glue_jobs/silver_to_gold.py` |

---

## Athena

| Resource | Terraform | Description |
|----------|-----------|-------------|
| Workgroup | `aws_athena_workgroup.retail` | `retail-analytics` |
| Result Location | S3 bucket | `s3://retail-athena-results-xxx/` |

**Tables**: Created via `sql/athena/create_external_tables.sql` or Glue Crawler.

---

## Lambda

| Resource | Terraform | Description |
|----------|-----------|-------------|
| Ingestion Function | `aws_lambda_function.ingestion` | Uploads sample data to raw S3 |
| Handler | `ingestion.lambda.app.lambda_handler` | |
| Runtime | Python 3.11 | |

---

## EventBridge

| Resource | Terraform | Description |
|----------|-----------|-------------|
| Schedule | `aws_cloudwatch_event_rule.ingestion_schedule` | Triggers Lambda (e.g. daily) |
| Target | Lambda ingestion function | |

---

## IAM Roles

| Role | Purpose |
|------|---------|
| `glue-job-role` | Glue jobs: read S3, write S3, access Glue Catalog |
| `glue-crawler-role` | Glue crawlers: read S3, write Glue Catalog |
| `lambda-ingestion-role` | Lambda: write to raw S3 |
| `athena-role` | Athena: read S3, write results bucket |

---

## Region

- **Default**: `ap-southeast-2` (Sydney)
- **Terraform variable**: `aws_region`

---

## Production Checklist

- [ ] Enable S3 bucket versioning for raw/bronze/silver/gold
- [ ] Configure lifecycle rules for raw zone (e.g. transition to Glacier after 90 days)
- [ ] Enable Glue job bookmarking for incremental processing
- [ ] Set up CloudWatch alarms for Glue job failures
- [ ] Configure Athena query result encryption
- [ ] Use AWS Secrets Manager for any credentials (e.g. dbt profile)
