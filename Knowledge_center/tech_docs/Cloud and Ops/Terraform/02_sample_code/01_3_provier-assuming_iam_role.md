### Provider Assuming an IAM Role

This is a secure pattern where Terraform uses its initial credentials only to assume a specific IAM Role. That role then performs the actions. This is great for security and cross-account access.

```
# main.tf

terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

# This provider will first authenticate, then assume the specified IAM role.
# All subsequent actions will be performed by this role.

provider "aws" {
  region = "us-east-1"

  assume_role {
    # The Amazon Resource Name (ARN) of the role to assume.
    # This role must trust the user/role running Terraform.
    
    role_arn     = "arn:aws:iam::123456789012:role/TerraformExecutionRole"
    
    # A name for the session, useful for auditing in CloudTrail.
    
    session_name = "TERRAFORM_DEPLOYMENT"
  }
}

# This S3 bucket will be created by the assumed 'TerraformExecutionRole'.

resource "aws_s3_bucket" "secure_logs" {
  bucket = "my-secure-logs-bucket-created-by-role"
}
```
Explanation: The assume_role block tells the provider to get temporary credentials for the role specified in role_arn. This is the most secure method for production environments because it limits direct access and relies on temporary, role-based permissions. You must replace the placeholder role_arn with the actual ARN of a role in your AWS account.