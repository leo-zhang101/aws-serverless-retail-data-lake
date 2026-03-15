# Terraform Validation Checklist

## Resource Inventory

| Resource Type | Resource Name | Purpose |
|---------------|---------------|---------|
| aws_s3_bucket | raw | Incoming CSV files |
| aws_s3_bucket | bronze | Parquet from raw |
| aws_s3_bucket | silver | Cleaned Parquet |
| aws_s3_bucket | gold | Curated analytics tables |
| aws_s3_bucket | athena_results | Athena query output |
| aws_s3_bucket | glue_scripts | Glue job code + temp |
| aws_glue_catalog_database | retail | Glue catalog DB `retail_analytics` |
| aws_glue_job | raw_to_bronze | ETL: raw → bronze |
| aws_glue_job | bronze_to_silver | ETL: bronze → silver |
| aws_glue_job | silver_to_gold | ETL: silver → gold |
| aws_lambda_function | ingestion | Upload sample data to raw |
| aws_cloudwatch_event_rule | ingestion_schedule | Daily trigger for Lambda |
| aws_athena_workgroup | retail | Athena workgroup |

## Duplicate Check

- **aws_glue_catalog_database.retail**: Single definition in glue.tf
- **aws_s3_object** (glue scripts): One per script (raw_to_bronze, bronze_to_silver, silver_to_gold)
- **aws_glue_job**: One per ETL stage
- **archive_file / lambda**: Single definition in lambda.tf

## Glue Job Default Arguments

All three Glue jobs include `--LOAD_DATE` = "TODAY".

## Lambda Packaging

Single `archive_file` in lambda.tf: source_dir = repo root, excludes = infrastructure, glue_jobs, dbt, docs, sql, dashboards, .git, etc. Handler = `ingestion.lambda.app.lambda_handler`.

---

## Validation Steps

### 1. terraform fmt

```bash
cd infrastructure/terraform
terraform fmt -recursive
```

### 2. terraform init

```bash
terraform init
```

### 3. terraform validate

```bash
terraform validate
```

Expected: `Success! The configuration is valid.`

### 4. terraform plan

```bash
terraform plan -out=tfplan
```

Check for:
- No "duplicate resource" errors
- Glue scripts found at `../../glue_jobs/*.py`
- Lambda zip includes `ingestion/` and `sample_data/`

### 5. terraform apply

```bash
terraform apply
# or: terraform apply tfplan
```

Preconditions: AWS credentials, glue_jobs/*.py exist, sample_data/*.csv exist.

---

## Dependency Graph

```
main.tf (locals) → s3.tf, iam.tf, glue.tf, athena.tf, lambda.tf, eventbridge.tf
```

---

## Lambda Packaging

- source_dir: repo root (includes ingestion/, sample_data/)
- Handler: ingestion.lambda.app.lambda_handler (requires ingestion/__init__.py, ingestion/lambda/__init__.py)
