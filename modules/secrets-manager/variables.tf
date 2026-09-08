variable "project" {
  description = "Project name"
  type        = string
}

variable "env" {
  description = "Environment name (dev, qa, prod)"
  type        = string
}

variable "db_username" {
  description = "Database username to store in Secrets Manager"
  type        = string
  sensitive   = true
}

variable "db_password" {
  description = "Database password to share in Secrets Manager"
  type        = string
  sensitive   = true
}

variable "jwt_secret" {
  description = "JWT signin secret to store in Secrets Manager"
  type        = string
  sensitive   = true
}

variable "db_host" {
  description = "RDS endpoint hostname to store alongside credentials"
  type        = string
}
