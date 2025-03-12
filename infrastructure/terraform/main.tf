provider "aws" {
  region = var.aws_region
}

resource "aws_iam_role" "lambda_role" {
  name = "ebs-snapshot-cleanup-lambda-role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = "sts:AssumeRole"
        Effect = "Allow"
        Principal = {
          Service = "lambda.amazonaws.com"
        }
      }
    ]
  })
}

resource "aws_iam_role_policy" "lambda_policy" {
  name = "ebs-snapshot-cleanup-lambda-policy"
  role = aws_iam_role.lambda_role.id

  policy = file("${path.module}/../lambda_iam_role.json")
}

resource "aws_lambda_function" "ebs_snapshot_cleanup" {
  filename      = "lambda_function_payload.zip"
  function_name = "ebs-snapshot-cleanup"
  role          = aws_iam_role.lambda_role.arn
  handler       = "lambda_function.lambda_handler"
  runtime       = "python3.8"

  source_code_hash = filebase64sha256("lambda_function_payload.zip")

  environment {
    variables = {
      LOG_LEVEL = "INFO"
    }
  }
}

resource "aws_cloudwatch_event_rule" "daily_trigger" {
  name                = "ebs-snapshot-cleanup-rule"
  schedule_expression = "cron(0 0 * * ? *)"
}

resource "aws_cloudwatch_event_target" "lambda_target" {
  rule      = aws_cloudwatch_event_rule.daily_trigger.name
  target_id = "ebs-snapshot-cleanup-lambda"
  arn       = aws_lambda_function.ebs_snapshot_cleanup.arn
}

resource "aws_lambda_permission" "allow_cloudwatch" {
  statement_id  = "AllowExecutionFromCloudWatch"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.ebs_snapshot_cleanup.function_name
  principal     = "events.amazonaws.com"
  source_arn    = aws_cloudwatch_event_rule.daily_trigger.arn
}