variable "db_password" {
    description = "Master password for the RDS PostgreSQL database"
    type = string
    sensitive = true
}

variable "jwt_secret" {
    description = "JWT signinf secret for the application"
    type = string
    sensitive = true
}

variable "github_org" {
    description = "Github username or organization that owns frontend and backend"
    type = string
    default = "zenpharma"
}