output "lambda_function_name" {
  description = "Name of the Lambda function"
  value       = aws_lambda_function.ebs_snapshot_cleanup.function_name
}

output "cloudwatch_event_rule_name" {
  description = "Name of the CloudWatch Event Rule"
  value       = aws_cloudwatch_event_rule.daily_trigger.name
}