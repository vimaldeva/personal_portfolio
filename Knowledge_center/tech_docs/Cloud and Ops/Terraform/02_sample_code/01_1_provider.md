### Providers

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

# Basic provider configuration for a single region.

# Terraform will automatically use credentials from environment variables

# or the shared credentials file (~/.aws/credentials).

provider "aws" {
  region = "us-east-1"
}

# This resource will be created in the us-east-1 region
# as defined in the provider block above.

resource "aws_s3_bucket" "example" {
  bucket = "my-tf-single-region-bucket-example"
}
```