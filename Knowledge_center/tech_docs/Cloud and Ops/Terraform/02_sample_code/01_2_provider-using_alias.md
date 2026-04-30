### Proviers - using alias

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

# 1. Default provider (no alias)
provider "aws" {
  region = "us-east-1"
}

# 2. Secondary provider with a unique name ("alias")

provider "aws" {
  alias  = "west_region"
  region = "us-west-2"
}

# This resource uses the default provider and will be created in us-east-1.

resource "aws_instance" "main_app_server" {
  ami           = "ami-0c55b159cbfafe1f0" # An Amazon Linux 2 AMI in us-east-1
  instance_type = "t2.micro"

  tags = {
    Name = "Primary Server (us-east-1)"
  }
}

# This resource explicitly uses the aliased provider via the 'provider' meta-argument.
# It will be created in the us-west-2 region.

resource "aws_instance" "dr_server" {
  provider = aws.west_region # Tells Terraform to use the aliased provider

  ami           = "ami-0c55b159cbfafe1f0" # An Amazon Linux 2 AMI in us-west-2
  instance_type = "t2.micro"

  tags = {
    Name = "DR Server (us-west-2)"
  }
}

```