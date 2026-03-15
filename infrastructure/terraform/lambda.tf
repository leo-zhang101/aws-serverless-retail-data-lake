# Lambda: zips repo root so sample_data/ is included. Excludes infra, glue, dbt, docs.

data "archive_file" "lambda_zip" {
  type        = "zip"
  source_dir  = "${path.module}/../.."
  output_path = "${path.module}/lambda_ingestion.zip"
  excludes    = ["infrastructure", "glue_jobs", "dbt", "docs", "sql", "dashboards", ".git", ".gitignore", ".terraform", "lambda_ingestion.zip"]
}

resource "aws_lambda_function" "ingestion" {
  filename         = data.archive_file.lambda_zip.output_path
  function_name    = "${local.name_prefix}-ingestion-${local.suffix}"
  role             = aws_iam_role.lambda_ingestion.arn
  handler          = "ingestion.lambda.app.lambda_handler"
  source_code_hash = data.archive_file.lambda_zip.output_base64sha256
  runtime          = "python3.11"
  timeout          = 60
  memory_size      = 256

  environment {
    variables = {
      RAW_BUCKET = aws_s3_bucket.raw.id
    }
  }
}
