# Security Group Configuration

# Security Group for RDS DB
resource "aws_security_group" "rds_sg" {
  vpc_id = aws_vpc.main_vpc.id

  ingress {
    from_port       = 0
    to_port         = 65535
    protocol        = "tcp"
    security_groups = [aws_security_group.lambda_sg.id]
  }

  ingress {
    from_port   = 3306
    to_port     = 3306
    protocol    = "tcp"
    cidr_blocks = ["10.0.0.0/16"]  # Allow access from within the VPC
  }

  ingress {
    from_port   = 3306
    to_port     = 3306
    protocol    = "tcp"
    cidr_blocks = [var.cidr_block, "128.189.204.245/32"] # Allow traffic from my IP Address & UBC
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"] # Allow all outgoing traffic
  }

  tags = {
    Name    = "${var.app_prefix}-rds-sg"
    Project = var.app_name
  }
}

# Security Group for Backend Lambda
resource "aws_security_group" "lambda_sg" {
  vpc_id = aws_vpc.main_vpc.id

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"] # Allow all outgoing traffic
  }

  tags = {
    Name    = "${var.app_prefix}-lambda-sg"
    Project = var.app_name
  }
}
