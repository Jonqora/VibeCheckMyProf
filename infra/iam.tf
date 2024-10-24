# Drafted IAM Roles For Authentication and Access Control

# IAM Role for Lambda to Access RDS
resource "aws_iam_role" "lambda_rds_role" {
  name = "${var.application_name}-lambda-rds-access-role"

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

resource "aws_iam_policy" "lambda_rds_policy" {
  name        = "${var.application_name}-lambda-rds-policy"
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
}

resource "aws_iam_role_policy_attachment" "lambda_rds_attach" {
  role       = aws_iam_role.lambda_rds_role.name
  policy_arn = aws_iam_policy.lambda_rds_policy.arn
}

# IAM Role for EC2 to Access RDS
resource "aws_iam_role" "ec2_rds_role" {
  name = "${var.application_name}-ec2-rds-access-role"

  assume_role_policy = jsonencode({
    "Version": "2012-10-17",
    "Statement": [
      {
        "Effect": "Allow",
        "Principal": {
          "Service": "ec2.amazonaws.com"
        },
        "Action": "sts:AssumeRole"
      }
    ]
  })
}

resource "aws_iam_policy" "ec2_rds_policy" {
  name        = "${var.application_name}-ec2-rds-policy"
  description = "Policy for EC2 to access RDS MySQL and Secrets Manager"

  policy = jsonencode({
    "Version": "2012-10-17",
    "Statement": [
      {
        "Effect": "Allow",
        "Action": [
          "rds-db:connect",  # Allows EC2 to connect to the RDS database
          "secretsmanager:GetSecretValue"  # Allows EC2 to retrieve secrets from Secrets Manager
        ],
        "Resource": [
          "${aws_db_instance.mysql-rds-db.arn}:dbuser:${var.database_user}",  # Use RDS db ARN
          aws_secretsmanager_secret.db_credentials.arn  # Refers to the secret ARN created by Terraform
        ]
      }
    ]
  })
}

resource "aws_iam_role_policy_attachment" "ec2_rds_attach" {
  role       = aws_iam_role.ec2_rds_role.name
  policy_arn = aws_iam_policy.ec2_rds_policy.arn
}

# IAM Role for Lambda to Access S3
# resource "aws_iam_role" "lambda_s3_role" {
#   name = "${var.application_name}-lambda-s3-access-role"
#
#   assume_role_policy = jsonencode({
#     "Version": "2012-10-17",
#     "Statement": [
#       {
#         "Effect": "Allow",
#         "Principal": {
#           "Service": "lambda.amazonaws.com"
#         },
#         "Action": "sts:AssumeRole"
#       }
#     ]
#   })
# }
#
# resource "aws_iam_policy" "lambda_s3_policy" {
#   name        = "${var.application_name}-lambda-s3-policy"
#   description = "Policy for Lambda to access S3 bucket"
#
#   policy = jsonencode({
#     "Version": "2012-10-17",
#     "Statement": [
#       {
#         "Effect": "Allow",
#         "Action": [
#           "s3:GetObject",  # Allows Lambda to read from S3 bucket
#           "s3:PutObject"   # Allows Lambda to write to S3 bucket
#         ],
#         "Resource": "arn:aws:s3:::my-bucket-name/*"  # TODO: Replace 'my-bucket-name' with actual S3 bucket name
#       }
#     ]
#   })
# }
#
# resource "aws_iam_role_policy_attachment" "lambda_s3_attach" {
#   role       = aws_iam_role.lambda_s3_role.name
#   policy_arn = aws_iam_policy.lambda_s3_policy.arn
# }
