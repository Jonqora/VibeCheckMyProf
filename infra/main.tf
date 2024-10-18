# AWS Resource Infrastructure/Configuration
terraform {
  required_providers {
    aws = {
      source = "hashicorp/aws"
    }
  }
}
provider "aws" {
  region = var.aws_region
}

# Create a DB Subnet Group for the RDS instance
resource "aws_db_subnet_group" "rds_subnet_group" {
  name       = "rds_subnet_group"
  subnet_ids = ["subnet-01326c48a15781a87", "subnet-05247d8d4578e61d3", "subnet-065f135448f443d0e",
                "subnet-0d133c7f3ebeca3a6", "subnet-0ceed7babb2e1347e", "subnet-00582fbe1f26f8f74"]
  description = "Subnet group for the RDS instance"

  tags = {
    Name = "rds_subnet_group"
  }
}

# Create a Security Group for the RDS instance
resource "aws_security_group" "rds_sg" {
  name        = "rds_security_group"
  description = "Inbound and outbound traffic rules for the RDS Database"
  vpc_id      = "vpc-06ff65fe48934d3af"

  # Limit incoming traffic to set of IP Addresses
  ingress {
    from_port   = 3306
    to_port     = 3306
    protocol    = "tcp"
    cidr_blocks = [var.cidr_block]
  }

  # Allow all outgoing traffic
  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

# Create a MySQL RDS instance using Free Tier Configuration
resource "aws_db_instance" "mysql-rds" {
  allocated_storage       = 20                                         # Storage size in GB
  storage_type            = "gp2"                                      # General Purpose SSD
  engine                  = "mysql"                                    # Database engine
  engine_version          = "8.0"                                      # MySQL version
  instance_class          = "db.t4g.micro"                             # Instance type
  identifier              = var.database_name                          # DB Instance ID
  db_name                 = var.database_name                          # Name of the database
  username                = var.database_user                          # Master username
  password                = var.database_password                      # Master password
  parameter_group_name    = "default.mysql8.0"                         # MySQL parameter group
  skip_final_snapshot     = true                                       # Skip final snapshot on deletion
  publicly_accessible     = true                                       # Whether the DB is publicly accessible
  port                    = 3306                                       # MySQL port
  backup_retention_period = 7                                          # Backup retention in days
  vpc_security_group_ids  = [aws_security_group.rds_sg.id]             # Attach the Security Group defined above
  db_subnet_group_name    = aws_db_subnet_group.rds_subnet_group.name  # Reference the DB subnet group

}

# Output the RDS endpoint
output "rds_endpoint" {
  description = "The endpoint of the RDS instance"
  value       = aws_db_instance.mysql-rds.endpoint
}