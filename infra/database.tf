# Create a MySQL RDS instance using Free Tier Configuration
resource "aws_db_instance" "mysql-rds-db" {
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
  vpc_security_group_ids  = [aws_security_group.backend_sg.id]         # Allow access from backend only
  db_subnet_group_name    = aws_db_subnet_group.rds_subnet_group.name  # Reference the DB subnet group
  tags = {
    name = "${var.application_name}-db"
  }
}