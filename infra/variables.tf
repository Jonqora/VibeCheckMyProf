# Definitions of variables used in the main.tf file

variable "cidr_block" {
  description = "The IP address allowed to access the database"
  type        = string
}

variable "database_name" {
  description = "The name of the database to create"
  type        = string
}

variable "database_user" {
  description = "The database master username"
  type        = string
  default     = "admin"
}

variable "database_password" {
  description = "The database master password"
  type        = string
  sensitive   = true # This variable is marked as sensitive so it's not displayed in logs
}

variable "aws_region" {
  description = "AWS region to deploy the RDS instance"
  type        = string
  default     = "ca-central-1"
}