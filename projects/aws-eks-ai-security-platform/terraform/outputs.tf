output "cluster_name" {
  value       = aws_eks_cluster.this.name
  description = "EKS cluster name."
}
output "cluster_endpoint" {
  value       = aws_eks_cluster.this.endpoint
  description = "Private Kubernetes API endpoint."
}
output "vpc_id" {
  value       = aws_vpc.this.id
  description = "VPC identifier."
}
output "ai_inference_role_arn" {
  value       = aws_iam_role.ai_inference.arn
  description = "IRSA role ARN for ai-inference/ai-inference-sa."
}
