# Security Group Configuration

# Create Security Group for Lambda
resource "aws_security_group" "lambda_sg" {
  name        = "lambda_sg"
  description = "Allow Lambda access to RDS"
  vpc_id      = aws_vpc.main.id

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

# Create Security Group for RDS
resource "aws_security_group" "rds_sg" {
  name        = "rds_sg"
  description = "Allow RDS access only from Lambda"
  vpc_id      = aws_vpc.main.id

  ingress {
    from_port       = 3306                  # MySQL port (adjust for your database type)
    to_port         = 3306
    protocol        = "tcp"
    security_groups = [aws_security_group.lambda_sg.id]  # Only allow access from Lambda SG
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}
