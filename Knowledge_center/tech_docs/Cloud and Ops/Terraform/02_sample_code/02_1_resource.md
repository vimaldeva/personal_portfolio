### Resource

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

# A basic EC2 instance resource
resource "aws_instance" "web" {
  ami           = "ami-0c55b159cbfafe1f0"  # Amazon Linux 2 AMI
  instance_type = "t2.micro"

  tags = {
    Name = "MyWebServer"
  }
}

# A basic S3 bucket resource
resource "aws_s3_bucket" "data" {
  bucket = "my-terraform-data-bucket-12345"

  tags = {
    Environment = "Development"
  }
}

```