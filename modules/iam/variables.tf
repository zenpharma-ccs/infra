variable "project" {
    description = "Project name"
    type = string
}

variable "env" {
    description = "Environment name (dev, qa, prod)"
    type = string
}

variable "oidc_provider_arn" {
    description = "ARN of the EKS OIDC provider"
    type = string
}

variable "oidc_provider_url" {
    description = "URL of the EKS OIDC provider"
    type = string
}

variable "aws_account_id" {
    description = "AWS Account id"
    type = string
}

variable "github_org" {
    description = "Github organization or username that owns the frontend and backend"
    type = string
}