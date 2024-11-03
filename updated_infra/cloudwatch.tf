
# Create EventBridge Rule to Schedule Preload Lambda
resource "aws_cloudwatch_event_rule" "schedule_rule" {
  name                 = "preload-professor-data-schedule"
  schedule_expression  = "rate(1 hour)"  # Change as needed
}

resource "aws_cloudwatch_event_target" "schedule_target" {
  rule      = aws_cloudwatch_event_rule.schedule_rule.name
  arn       = aws_lambda_function.preload_professor_data.arn
}

resource "aws_lambda_permission" "allow_cloudwatch_invoke" {
  statement_id  = "AllowExecutionFromCloudWatch"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.preload_professor_data.function_name
  principal     = "events.amazonaws.com"
  source_arn    = aws_cloudwatch_event_rule.schedule_rule.arn
}