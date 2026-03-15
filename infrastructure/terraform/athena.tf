# Athena Workgroup for Retail Analytics

resource "aws_athena_workgroup" "retail" {
  name        = "${local.name_prefix}-athena-${local.suffix}"
  description = "Retail analytics queries - serverless-aws-data-platform"

  configuration {
    enforce_workgroup_configuration    = true
    publish_cloudwatch_metrics_enabled = true

    result_configuration {
      output_location = "s3://${aws_s3_bucket.athena_results.id}/athena-results/"
      encryption_configuration {
        encryption_option = "SSE_S3"
      }
    }
  }
}
