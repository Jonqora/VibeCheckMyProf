# IAM Role For Authentication and Access Control

# Create IAM Role for Lambda to Access RDS
resource "aws_iam_role" "lambda_rds_role" {
  name = "${var.app_prefix}-lambda-rds-access-role"

  assume_role_policy = jsonencode({
    "Version": "2012-10-17",
    "Statement": [
      {
        "Effect": "Allow",
        "Principal": {
          "Service": "lambda.amazonaws.com"
        },
        "Action": "sts:AssumeRole"
      }
    ]
  })

  tags = {
    Name        = "${var.app_prefix}-lambda-rds-role"
    Project     = var.app_name
  }
}

# Create IAM Policy for Lambda-RDS Access
resource "aws_iam_policy" "lambda_rds_policy" {
  name        = "${var.app_prefix}-lambda-rds-policy"
  description = "Policy for Lambda to access RDS MySQL and Secrets Manager"

  policy = jsonencode({
    "Version": "2012-10-17",
    "Statement": [
      {
        "Effect": "Allow",
        "Action": [
          "rds-db:connect",  # Allows Lambda to connect to the RDS database
          "secretsmanager:GetSecretValue"  # Allows Lambda to retrieve secrets from Secrets Manager
        ],
        "Resource": [
          "${aws_db_instance.mysql-rds-db.arn}:dbuser:${var.database_user}",  # Use RDS db ARN
          aws_secretsmanager_secret.db_credentials.arn  # Refers to the secret ARN created by Terraform
        ]
      },
      {
        "Effect": "Allow",
        "Action": [
          "logs:CreateLogGroup",
          "logs:CreateLogStream",
          "logs:PutLogEvents"
        ],
        "Resource": "*"  # This allows Lambda to create log groups and log events in CloudWatch
      }
    ]
  })

  tags = {
    Name        = "${var.app_prefix}-lambda-rds-role"
    Project     = var.app_name
  }
}

# Attach Role to RDS Resource
resource "aws_iam_role_policy_attachment" "lambda_rds_attach" {
  role       = aws_iam_role.lambda_rds_role.name
  policy_arn = aws_iam_policy.lambda_rds_policy.arn
}
