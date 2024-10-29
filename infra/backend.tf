# TODO: Finish configuration with zip of backend app files

# # Backend Configuration - Lambda Function

# data "archive_file" "lambda" {
#   type        = "zip"
#   source_file = "script.py"
#   output_path = "lambda_function_payload.zip"
# }
#
# # Create Backend Lambda
# resource "aws_lambda_function" "backend_lambda" {
#   function_name = var.application_name
#   role          = aws_iam_role.lambda_rds_role.arn
#   handler       = "app.handler" # TODO: Add handler function
#   runtime       = "python3.8"   # TODO: Specify runtime
#   filename      = "database/script.py" # TODO: Add script to zip/containerize backend
#
#   # Specify Environment Variable Values to Use in Database Connection
#   environment {
#     variables = {
#       DB_HOST     = aws_db_instance.mysql-rds-db.endpoint # Endpoint of RDS Instance
#       DB_USER     = var.database_user
#       DB_NAME     = var.database_name
#       DB_PASSWORD = var.database_password # TODO: Replace with Secrets Manager?
#     }
#   }
#
#   tags = {
#     Name    = "${var.app_prefix}-backend-lambda"
#     Project = var.application_name
#   }
# }