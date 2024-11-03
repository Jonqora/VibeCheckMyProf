# IAM Role For Authentication and Access Control

# Create IAM Role for Lambda
resource "aws_iam_role" "lambda_execution_role" {
  name = "lambda_execution_role"
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
}

# Create Policy for Lambda
resource "aws_iam_policy" "lambda_vpc_access_policy" {
  name        = "LambdaVpcAccessPolicy"
  description = "Allows Lambda to manage network interfaces in a VPC and access RDS"
  policy      = jsonencode({
    "Version": "2012-10-17",
    "Statement": [
      {
        "Effect": "Allow",
        "Action": [
          "ec2:CreateNetworkInterface",
          "ec2:DescribeNetworkInterfaces",
          "ec2:DeleteNetworkInterface",
          "rds-db:connect",
          "secretsmanager:GetSecretValue"
        ],
        "Resource": "*"
      }
    ]
  })
}

# Attach Lambda Role to Policy
resource "aws_iam_role_policy_attachment" "lambda_basic_execution" {
  role       = aws_iam_role.lambda_execution_role.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole"
}

resource "aws_iam_role_policy_attachment" "lambda_vpc_access" {
  role       = aws_iam_role.lambda_execution_role.name
  policy_arn = aws_iam_policy.lambda_vpc_access_policy.arn
}