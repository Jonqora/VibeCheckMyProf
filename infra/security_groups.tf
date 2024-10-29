# Security Group Configuration

# Security Group for RDS DB
resource "aws_security_group" "rds_sg" {
  vpc_id = aws_vpc.main_vpc.id

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
    cidr_blocks = [var.cidr_block] # Allow traffic from my IP Address
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"] # Allow all outgoing traffic
  }

  tags = {
    Name    = "rds-sg"
    Project = var.application_name
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
    Name    = "lambda-sg"
    Project = var.application_name
  }
}


# # Security Group for Web Server (allow HTTP/HTTPS)
# resource "aws_security_group" "web_sg" {
#   vpc_id = aws_vpc.web_app_vpc.id
#
#   ingress {
#     from_port   = 80
#     to_port     = 80
#     protocol    = "tcp"
#     cidr_blocks = ["0.0.0.0/0"]  # Allow HTTP from anywhere
#   }
#
#   ingress {
#     from_port   = 443
#     to_port     = 443
#     protocol    = "tcp"
#     cidr_blocks = ["0.0.0.0/0"]  # Allow HTTPS from anywhere
#   }
#
#   egress {
#     from_port   = 0
#     to_port     = 0
#     protocol    = "-1"  # Allow all outbound traffic
#     cidr_blocks = ["0.0.0.0/0"]
#   }
#
#   tags = {
#     Name = "${var.application_name}-web-server-sg"
#   }
# }
#
# # Security Group for Backend (allow access from web server and personal IP)
# resource "aws_security_group" "backend_sg" {
#   vpc_id = aws_vpc.web_app_vpc.id
#
#   # Allow only web server access
#   ingress {
#     from_port   = 0
#     to_port     = 65535
#     protocol    = "tcp"
#     security_groups = [aws_security_group.web_sg.id]  # Allow only web server access
#   }
#
#   # Allow incoming traffic from my IP Address
#   ingress {
#     from_port   = 3306
#     to_port     = 3306
#     protocol    = "tcp"
#     cidr_blocks = [var.cidr_block]
#   }
#
#   egress {
#     from_port   = 0
#     to_port     = 0
#     protocol    = "-1"  # Allow all outbound traffic
#     cidr_blocks = ["0.0.0.0/0"]
#   }
#
#   tags = {
#     Name = "${var.application_name}-backend-sg"
#   }
# }
