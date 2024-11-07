# RDS Database Configuration

# Create a MySQL RDS instance using Free Tier Configuration
resource "aws_db_instance" "mysql-rds-db" {
  allocated_storage                   = 20                                         # Storage size in GB
  storage_type                        = "gp2"                                      # General Purpose SSD
  engine                              = "mysql"                                    # Database engine
  engine_version                      = "8.0"                                      # MySQL version
  instance_class                      = "db.t4g.micro"                             # Instance type
  identifier                          = var.database_name                          # DB Instance ID
  db_name                             = var.database_name                          # Name of the database
  username                            = var.database_user                          # Master username
  password                            = var.database_password                      # Master password
  parameter_group_name                = "default.mysql8.0"                         # MySQL parameter group
  iam_database_authentication_enabled = true                                       # Allow mapping of IAM to db
  skip_final_snapshot                 = true                                       # Skip final snapshot on deletion
  # TODO: Remove public access when development is complete?
  publicly_accessible                 = true                                       # Make DB is publicly accessible
  port                                = 3306                                       # MySQL port
  backup_retention_period             = 7                                          # Backup retention in days
  vpc_security_group_ids              = [                                          # Allow access from backend only
                                        aws_security_group.rds_sg.id,
                                        aws_security_group.rds_sg_grafana1.id,
                                        aws_security_group.rds_sg_grafana2.id,
                                        aws_security_group.rds_sg_grafana3.id
                                        ]
  db_subnet_group_name                = aws_db_subnet_group.rds_subnet_group.name  # Reference the DB subnet group

  tags = {
    Name    = "${var.app_prefix}-rds-db"
    Project = var.app_name
  }
}