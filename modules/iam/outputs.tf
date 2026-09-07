output "eso_role_arn" {
    description = "ARN of the External Secrets Operator IAM Role"
    value = aws_iam_role.eso_role.arn
}

output "argocd_role_arn" {
    description = "ARN of the ArgoCD Iam Role"
    value = aws_iam_role.argocd_role.arn
}

output "alb_controller_role_arn" {
    description = "ARN of the AWS Load Balancer Controller IAM Role"
    value = aws_iam_role.alb_controller_role.arn
}