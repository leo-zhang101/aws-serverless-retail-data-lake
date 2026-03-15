# Root module. suffix = short hash for globally unique bucket names.
data "aws_caller_identity" "current" {}
data "aws_region" "current" {}

locals {
  account_id = data.aws_caller_identity.current.account_id
  region     = data.aws_region.current.name
  # Short suffix for resource naming (globally unique per project/env/account)
  suffix = substr(md5("${var.project_name}-${var.environment}-${local.account_id}"), 0, 8)
  # Unified resource name prefix: project-environment-resource-suffix
  name_prefix = "${var.project_name}-${var.environment}"
}
