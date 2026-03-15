# Glue DB + 3 ETL jobs. LOAD_DATE=TODAY lets re-run for specific date via job params.
# job-bookmark-enable: Glue tracks progress; we don't use it for partition-based reads but it's harmless.
resource "aws_glue_catalog_database" "retail" {
  name        = "retail_analytics"
  description = "Retail analytics data lake - Glue catalog database"
}

locals {
  glue_script_path = "${path.module}/../../glue_jobs"
  glue_job_common_args = {
    "--job-language"                         = "python"
    "--job-bookmark-option"                  = "job-bookmark-enable"
    "--enable-metrics"                       = "true"
    "--enable-continuous-cloudwatch-logging" = "true"
    "--enable-spark-ui"                      = "true"
    "--spark-event-logs-path"                = "s3://${aws_s3_bucket.glue_scripts.id}/spark-logs/"
    "--TempDir"                              = "s3://${aws_s3_bucket.glue_scripts.id}/temp/"
    "--GLUE_DATABASE"                        = aws_glue_catalog_database.retail.name
  }
}

resource "aws_s3_object" "glue_raw_to_bronze" {
  bucket = aws_s3_bucket.glue_scripts.id
  key    = "glue_jobs/raw_to_bronze.py"
  source = "${local.glue_script_path}/raw_to_bronze.py"
  etag   = filemd5("${local.glue_script_path}/raw_to_bronze.py")
}

resource "aws_s3_object" "glue_bronze_to_silver" {
  bucket = aws_s3_bucket.glue_scripts.id
  key    = "glue_jobs/bronze_to_silver.py"
  source = "${local.glue_script_path}/bronze_to_silver.py"
  etag   = filemd5("${local.glue_script_path}/bronze_to_silver.py")
}

resource "aws_s3_object" "glue_silver_to_gold" {
  bucket = aws_s3_bucket.glue_scripts.id
  key    = "glue_jobs/silver_to_gold.py"
  source = "${local.glue_script_path}/silver_to_gold.py"
  etag   = filemd5("${local.glue_script_path}/silver_to_gold.py")
}

resource "aws_glue_job" "raw_to_bronze" {
  name     = "${local.name_prefix}-raw-to-bronze-${local.suffix}"
  role_arn = aws_iam_role.glue_job.arn

  command {
    name            = "glueetl"
    script_location = "s3://${aws_s3_bucket.glue_scripts.id}/${aws_s3_object.glue_raw_to_bronze.key}"
    python_version  = "3"
  }

  default_arguments = merge(local.glue_job_common_args, {
    "--RAW_BUCKET"    = aws_s3_bucket.raw.id
    "--BRONZE_BUCKET" = aws_s3_bucket.bronze.id
    "--LOAD_DATE"     = "TODAY"
  })

  worker_type       = var.glue_job_worker_type
  number_of_workers = var.glue_job_number_of_workers
  glue_version      = "4.0"
  timeout           = 60
}

resource "aws_glue_job" "bronze_to_silver" {
  name     = "${local.name_prefix}-bronze-to-silver-${local.suffix}"
  role_arn = aws_iam_role.glue_job.arn

  command {
    name            = "glueetl"
    script_location = "s3://${aws_s3_bucket.glue_scripts.id}/${aws_s3_object.glue_bronze_to_silver.key}"
    python_version  = "3"
  }

  default_arguments = merge(local.glue_job_common_args, {
    "--BRONZE_BUCKET" = aws_s3_bucket.bronze.id
    "--SILVER_BUCKET" = aws_s3_bucket.silver.id
    "--LOAD_DATE"     = "TODAY"
  })

  worker_type       = var.glue_job_worker_type
  number_of_workers = var.glue_job_number_of_workers
  glue_version      = "4.0"
  timeout           = 60
}

resource "aws_glue_job" "silver_to_gold" {
  name     = "${local.name_prefix}-silver-to-gold-${local.suffix}"
  role_arn = aws_iam_role.glue_job.arn

  command {
    name            = "glueetl"
    script_location = "s3://${aws_s3_bucket.glue_scripts.id}/${aws_s3_object.glue_silver_to_gold.key}"
    python_version  = "3"
  }

  default_arguments = merge(local.glue_job_common_args, {
    "--SILVER_BUCKET" = aws_s3_bucket.silver.id
    "--GOLD_BUCKET"   = aws_s3_bucket.gold.id
    "--LOAD_DATE"     = "TODAY"
  })

  worker_type       = var.glue_job_worker_type
  number_of_workers = var.glue_job_number_of_workers
  glue_version      = "4.0"
  timeout           = 60
}
