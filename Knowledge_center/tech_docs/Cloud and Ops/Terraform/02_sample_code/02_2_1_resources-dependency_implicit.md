### Resources - Implicit dependency

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

provider "aws" {
  region = "us-east-1"
}

# Create a VPC first

resource "aws_vpc" "main" {
  cidr_block = "10.0.0.0/16"

  tags = {
    Name = "MainVPC"
  }
}

# Create a subnet inside the VPC.
# Terraform automatically knows to create the VPC first because
# this subnet references the VPC's ID.

resource "aws_subnet" "public" {
  vpc_id     = aws_vpc.main.id  # Reference to VPC resource
  cidr_block = "10.0.1.0/24"

  tags = {
    Name = "PublicSubnet"
  }
}

# Create an EC2 instance in the subnet.
# Implicit dependency: Terraform sees we reference the subnet ID,
# so it will create VPC → Subnet → Instance in that order.

resource "aws_instance" "app" {
  ami           = "ami-0c55b159cbfafe1f0"
  instance_type = "t2.micro"
  subnet_id     = aws_subnet.public.id  # Reference to Subnet resource

  tags = {
    Name = "AppServer"
  }
}
```