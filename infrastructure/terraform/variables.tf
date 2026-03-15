variable "project_name" {
  description = "Project name used for resource naming"
  type        = string
  default     = "retail-analytics"
}

variable "environment" {
  description = "Environment (dev, staging, prod)"
  type        = string
  default     = "dev"
}

variable "aws_region" {
  description = "AWS region (ap-southeast-2 for Sydney)"
  type        = string
  default     = "ap-southeast-2"
}

variable "glue_job_worker_type" {
  description = "Glue job worker type (G.1X, G.2X)"
  type        = string
  default     = "G.1X"
}

variable "glue_job_number_of_workers" {
  description = "Number of Glue job workers"
  type        = number
  default     = 2
}
