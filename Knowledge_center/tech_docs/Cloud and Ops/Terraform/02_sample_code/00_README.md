### main.tf

This file is the core of your configuration. It defines the cloud provider and the resources you want to create.

```
# Configures the Terraform version and the required AWS provider.
terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

# Configures the AWS provider, setting the region where resources will be created.
provider "aws" {
  region = "us-east-1"
}

# A data source to dynamically find the latest Amazon Linux 2 AMI.
# This avoids hardcoding an AMI ID, which can become outdated.
data "aws_ami" "amazon_linux_2" {
  most_recent = true
  owners      = ["amazon"]

  filter {
    name   = "name"
    values = ["amzn2-ami-hvm-*-x86_64-gp2"]
  }
}

# Defines the EC2 instance resource. [5]
resource "aws_instance" "web_server" {
  # The AMI to use for the instance. We use the ID from our data source.
  ami           = data.aws_ami.amazon_linux_2.id
  
  # The size of the instance. This is passed in from a variable.
  instance_type = var.instance_type

  # Tags are key-value pairs that help you manage, identify, and filter resources.
  tags = {
    Name    = "ExampleWebServer"
    Project = "Terraform-Tutorial"
  }
}
```

---
### variables.tf

This file defines the input variables for your configuration. Using variables makes your code more flexible and reusable, as you can change values without editing the main resource code.

```
# Defines a variable for the EC2 instance type.
variable "instance_type" {
  description = "The type of EC2 instance to provision."
  type        = string
  default     = "t2.micro"
}
```
---
### outputs.tf
This file declares the values that will be displayed after your infrastructure is successfully created. This is useful for retrieving information like IP addresses or instance IDs.
```
# Outputs the public IP address of the created EC2 instance.
output "instance_public_ip" {
  description = "Public IP address of the EC2 instance."
  value       = aws_instance.web_server.public_ip
}

# Outputs the unique ID of the created EC2 instance.
output "instance_id" {
  description = "ID of the EC2 instance."
  value       = aws_instance.web_server.id
}
```

### Explanation

**main.tf** : This is where the main action happens.

- The terraform block specifies the version of the AWS provider we want to use.
The provider "aws" block tells Terraform that we are creating resources in AWS, specifically in the us-east-1 region.
- The data "aws_ami" block is a special kind of block that fetches information. Instead of hardcoding an Amazon Machine Image (AMI) ID, it dynamically looks up the latest available Amazon Linux 2 AMI. This is a best practice to ensure you're always using an up-to-date and valid image.
- The resource "aws_instance" "web_server" block is the declaration of the actual EC2 instance. It uses the AMI found by the data source and an instance_type that is supplied by a variable.

**variables.tf**: This file makes the code reusable. By defining instance_type here, you can easily launch a different-sized server by changing the variable's default value or by providing a new value when you run Terraform.

**outputs.tf**: After Terraform creates the EC2 instance, it will have a unique ID and a public IP address assigned by AWS. The output blocks make this information available on your terminal for immediate use, such as connecting to the instance via SSH.

To use this code, you would save these three files in the same directory, run terraform init to initialize the project, and then terraform apply to create the EC2 instance.

