variable "aws_region" {
  description = "AWS region for the sandbox platform."
  type        = string
  default     = "us-east-1"
}
variable "cluster_name" {
  description = "EKS cluster name."
  type        = string
  default     = "secure-ai-eks-lab"
}
variable "environment" {
  type    = string
  default = "lab"
}
variable "vpc_cidr" {
  type    = string
  default = "10.40.0.0/16"
}
variable "public_subnet_cidrs" {
  type    = list(string)
  default = ["10.40.0.0/20", "10.40.16.0/20"]
  validation {
    condition     = length(var.public_subnet_cidrs) == 2
    error_message = "Provide exactly two public subnet CIDRs."
  }
}
variable "private_subnet_cidrs" {
  type    = list(string)
  default = ["10.40.32.0/20", "10.40.48.0/20"]
  validation {
    condition     = length(var.private_subnet_cidrs) == 2
    error_message = "Provide exactly two private subnet CIDRs."
  }
}
variable "node_instance_types" {
  type    = list(string)
  default = ["m6i.large"]
}
variable "node_desired_size" {
  type    = number
  default = 2
}
variable "node_min_size" {
  type    = number
  default = 2
}
variable "node_max_size" {
  type    = number
  default = 3
}
