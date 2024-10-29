# Backend Configuration - Lambda Function

# Create Backend Lambda
resource "aws_lambda_function" "backend_lambda" {
  function_name = var.application_name
  role          = aws_iam_role.lambda_rds_role.arn
  handler       = "app.handler" # TODO: Add handler function
  runtime       = "python3.8"   # TODO: Specify runtime
  filename      = "lambda_function.zip" # TODO: Add script to zip/containerize backend

  # Specify Environment Variable Values to Use in Database Connection
  environment {
    variables = {
      DB_HOST     = aws_db_instance.mysql-rds-db.endpoint # Endpoint of RDS Instance
      DB_USER     = var.database_user
      DB_NAME     = var.database_name
      DB_PASSWORD = var.database_password # TODO: Replace with Secrets Manager
    }
  }

  tags = {
    Name = "backend-lambda"
    Project = var.application_name
  }
}