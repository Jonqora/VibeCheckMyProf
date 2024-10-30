# Definitions of variables for use in the application

variable "app_name" {
  description = "Application name to add to AWS resource tags"
  type        = string
  default     = "vibe-check-my-prof"
}

variable "app_prefix" {
  description = "Prefix to add to unique resource names"
  type        = string
  default     = "vcmp"
}

variable "database_name" {
  description = "Application database name"
  type        = string
  default     = "vibecheckmyprofdb"
}

variable "cidr_block" {
  description = "Personal public IP address for database access from local environment"
  type        = string
}

variable "database_user" {
  description = "The database master username"
  type        = string
  default     = "admin"
}

variable "database_password" {
  description = "The database master password (save for authenticating to the database later)"
  type        = string
  sensitive   = true # This variable is marked as sensitive so it's not displayed in logs
}

variable "database_secret_name" {
  description = "Name of the secret to authenticate to the RDS database instance"
  type        = string
  default     = "my-super-db-secret"
}

variable "aws_region" {
  description = "AWS region to deploy the resources"
  type        = string
  default     = "ca-central-1"
}
