# Run Checklist

| # | Step | Command / Action | Verify |
|---|------|------------------|--------|
| 1 | terraform fmt | `cd infrastructure/terraform && terraform fmt -recursive` | No errors |
| 2 | terraform init | `terraform init` | .terraform/ created |
| 3 | terraform validate | `terraform validate` | "Success! The configuration is valid." |
| 4 | terraform plan | `terraform plan -out=tfplan` | Plan shows create/update, no errors |
| 5 | terraform apply | `terraform apply tfplan` | All resources created |
| 6 | Lambda invoke | `aws lambda invoke --function-name $(terraform output -raw lambda_ingestion_name) --payload '{"load_date":"2024-03-14"}' response.json && cat response.json` | uploaded_count > 0 |
| 7 | Glue job 1 | `terraform output glue_job_names` then `aws glue start-job-run --job-name <first-name>` | Wait for SUCCEEDED |
| 8 | Glue job 2 | `aws glue start-job-run --job-name <second-name>` | Wait for SUCCEEDED |
| 9 | Glue job 3 | `aws glue start-job-run --job-name <third-name>` | Wait for SUCCEEDED |
| 10 | Athena DDL | Replace REPLACE_GOLD_BUCKET in create_external_tables.sql with `terraform output -raw gold_bucket`, run in Athena | Tables created |
| 11 | Athena MSCK | `MSCK REPAIR TABLE daily_sales;` (and other tables) | Partitions added |
| 12 | Athena queries | Run sample_analytics_queries.sql | Rows returned |
| 13 | Dashboard screenshots | Capture Athena results or QuickSight dashboards → dashboards/screenshots/ | daily_sales_dashboard.png, product_performance_dashboard.png, customer_value_dashboard.png |
