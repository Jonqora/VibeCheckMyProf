# Secrets Manager for Security Layer
#
# # Create Secret in Secrets Manager
# resource "aws_secretsmanager_secret" "db_credentials" {
#   name                    = var.database_secret_name  # The name of your secret
#   description             = "RDS MySQL database credentials for the application"
#   recovery_window_in_days = 0
#   tags = {
#     Name    = "${var.app_prefix}-db-secret"
#     Project = var.app_name
#   }
# }
#
# # Create the secret value (username and password)
# resource "aws_secretsmanager_secret_version" "db_credentials_version" {
#   secret_id = aws_secretsmanager_secret.db_credentials.id  # Links to the secret created above
#
#   secret_string = jsonencode({
#     username = var.database_user
#     password = var.database_password
#     host     = aws_db_instance.mysql-rds-db.endpoint
#   })
# }