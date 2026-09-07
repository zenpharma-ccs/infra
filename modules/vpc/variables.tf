variable "project" {
    description = "Project name"
    type = string
}

variable "env" {
    description = "Environment name (dev, qa, prod)"
    type = string
}

variable "region" {
    description = "AWS region"
    type = string
    default = "us-est-1"
}

variable "vpc_cidr" {
    description = "CIDR block for vpc"
    type = string
    default = "10.0.0.0/16"
}

variable "public_subnet_cidrs" {
    description = "CIDR block for public subnets"
    type = list(string)
}

variable "private_subnet_cidrs" {
    description = "CIDR blocks for private subnets"
    type = list(string)
}

variable "database_subnet_cidrs" {
    description = "CIDR blocks for database subnets (rds)"
    type = list(string)
}