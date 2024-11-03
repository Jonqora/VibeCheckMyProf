# Output values used to create database connection

output "website_url" {
  value = aws_s3_bucket_website_configuration.bucket_website_config.website_endpoint
  description = "URL for the frontend website hosted on S3"
}

# output "db_name" {
#   description = "The name of the database"
#   value       = aws_db_instance.mysql-rds-db.db_name
# }
#
# output "db_user" {
#   description = "Database master username"
#   value       = aws_db_instance.mysql-rds-db.username
# }
#
# output "db_password" {
#   description = "Database master password"
#   value       = aws_db_instance.mysql-rds-db.password
#   sensitive   = true
# }
#
# output "db_host" {
#   description = "The endpoint of the RDS instance"
#   value       = aws_db_instance.mysql-rds-db.endpoint
# }
#
# output "db_port" {
#   description = "The database port"
#   value       = aws_db_instance.mysql-rds-db.port
# }
#
# Output db connection values to config.env file
resource "local_file" "env_file" {
  content = <<-EOT
    DB_NAME=${var.database_name}
    DB_USER=${var.database_user}
    DB_PASSWORD=${aws_db_instance.professor_data.password}
    DB_HOST=${aws_db_instance.professor_data.endpoint}
    DB_PORT=${aws_db_instance.professor_data.port}
    DB_SECRET_NAME=${var.database_secret_name}
    DB_REGION_NAME=${var.aws_region}
    SECOND_INTERVAL=${var.seconds_interval}
  EOT
  filename = "config.env"
}
