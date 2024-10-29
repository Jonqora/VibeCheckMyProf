# Output the VPC ID
output "vpc_id" {
  value = aws_vpc.main_vpc.id
}

# Output the public subnet ID
output "public_subnet_id_1" {
  value = aws_subnet.public_subnet_1.id
}

# Output the public subnet ID
output "public_subnet_id_2" {
  value = aws_subnet.public_subnet_2.id
}

# Output the private subnet ID
output "private_subnet_id_1" {
  value = aws_subnet.private_subnet_1.id
}

# Output the private subnet ID
output "private_subnet_id_2" {
  value = aws_subnet.private_subnet_2.id
}

# Output the RDS endpoint
output "rds_endpoint" {
  description = "The endpoint of the RDS instance"
  value       = aws_db_instance.mysql-rds-db.endpoint
}

# Output the RDS arn
output "rds_arn" {
  description = "The arn of the RDS instance"
  value       = aws_db_instance.mysql-rds-db.arn
}