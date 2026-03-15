output "raw_bucket" {
  description = "S3 raw zone bucket name"
  value       = aws_s3_bucket.raw.id
}

output "bronze_bucket" {
  description = "S3 bronze zone bucket name"
  value       = aws_s3_bucket.bronze.id
}

output "silver_bucket" {
  description = "S3 silver zone bucket name"
  value       = aws_s3_bucket.silver.id
}

output "gold_bucket" {
  description = "S3 gold zone bucket name"
  value       = aws_s3_bucket.gold.id
}

output "athena_results_bucket" {
  description = "S3 bucket for Athena query results"
  value       = aws_s3_bucket.athena_results.id
}

output "glue_scripts_bucket" {
  description = "S3 bucket for Glue job scripts"
  value       = aws_s3_bucket.glue_scripts.id
}

output "glue_database" {
  description = "Glue catalog database name"
  value       = aws_glue_catalog_database.retail.name
}

output "athena_workgroup" {
  description = "Athena workgroup name"
  value       = aws_athena_workgroup.retail.name
}

output "lambda_ingestion_name" {
  description = "Lambda ingestion function name"
  value       = aws_lambda_function.ingestion.function_name
}

output "lambda_ingestion_arn" {
  description = "Lambda ingestion function ARN"
  value       = aws_lambda_function.ingestion.arn
}

output "glue_job_names" {
  description = "Glue ETL job names"
  value = [
    aws_glue_job.raw_to_bronze.name,
    aws_glue_job.bronze_to_silver.name,
    aws_glue_job.silver_to_gold.name
  ]
}

output "eventbridge_rule_name" {
  description = "EventBridge schedule rule name"
  value       = aws_cloudwatch_event_rule.ingestion_schedule.name
}

output "run_commands" {
  description = "Useful commands for post-deploy"
  value       = <<-EOT
    # Invoke Lambda ingestion (optional: pass load_date in payload):
    aws lambda invoke --function-name ${aws_lambda_function.ingestion.function_name} --payload '{"load_date":"2024-03-14"}' response.json

    # Run Glue jobs (in order):
    aws glue start-job-run --job-name ${aws_glue_job.raw_to_bronze.name}
    aws glue start-job-run --job-name ${aws_glue_job.bronze_to_silver.name}
    aws glue start-job-run --job-name ${aws_glue_job.silver_to_gold.name}
  EOT
}
