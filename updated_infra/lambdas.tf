
# Create the Preload Lambda Function
resource "aws_lambda_function" "preload_professor_data" {
  function_name = "preload-professor-data"
  role          = aws_iam_role.lambda_execution_role.arn
  package_type  = "Image"
  image_uri     = "183631308178.dkr.ecr.ca-central-1.amazonaws.com/preload-professor-data@sha256:2aa8a2a5e424102a3f8d9685da5a2be0d1008dd64762c09d103979d028a4245f"
  memory_size   = 512
  timeout       = 900  # Allows up to 15 minutes for full processing

  vpc_config {
    subnet_ids         = [aws_subnet.private_subnet.id]
    security_group_ids = [aws_security_group.lambda_sg.id]
  }

  # Specify Environment Variable Values to Use in Database Connection
  environment {
    variables = {
      DB_NAME     = var.database_name
      DB_USER     = var.database_user
      DB_PASSWORD = var.database_password
      DB_HOST     = aws_db_instance.professor_data.endpoint # Endpoint of RDS Instance
      DB_PORT = aws_db_instance.professor_data.port
      DB_SECRET_NAME="vcmp-db-secret"
      DB_REGION_NAME="ca-central-1"
      SECOND_INTERVAL = 86400
    }
  }
}

# Create On-Demand Lambda Function for API Gateway
resource "aws_lambda_function" "on_demand_professor_data" {
  function_name = "on-demand-professor-data"
  role          = aws_iam_role.lambda_execution_role.arn
  package_type  = "Image"
  image_uri = "add-image-uri"
  memory_size   = 512
  timeout       = 30

  vpc_config {
    subnet_ids         = [aws_subnet.private_subnet.id]
    security_group_ids = [aws_security_group.lambda_sg.id]
  }

    # Specify Environment Variable Values to Use in Database Connection
  environment {
    variables = {
      DB_NAME     = var.database_name
      DB_USER     = var.database_user
      DB_PASSWORD = var.database_password
      DB_HOST     = aws_db_instance.professor_data.endpoint # Endpoint of RDS Instance
      DB_PORT = aws_db_instance.professor_data.port
      DB_SECRET_NAME="vcmp-db-secret"
      DB_REGION_NAME="ca-central-1"
      SECOND_INTERVAL = 86400
    }
  }
}