# EventBridge Schedule - Daily trigger for Lambda ingestion

resource "aws_cloudwatch_event_rule" "ingestion_schedule" {
  name                = "${local.name_prefix}-ingestion-schedule-${local.suffix}"
  description         = "Trigger Lambda ingestion daily at 6am AEST (approx 8pm UTC)"
  schedule_expression = "cron(0 20 * * ? *)"
}

resource "aws_cloudwatch_event_target" "lambda_ingestion" {
  rule      = aws_cloudwatch_event_rule.ingestion_schedule.name
  target_id = "RetailIngestion"
  arn       = aws_lambda_function.ingestion.arn
}

resource "aws_lambda_permission" "eventbridge" {
  statement_id  = "AllowExecutionFromEventBridge-${local.suffix}"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.ingestion.function_name
  principal     = "events.amazonaws.com"
  source_arn    = aws_cloudwatch_event_rule.ingestion_schedule.arn
}
