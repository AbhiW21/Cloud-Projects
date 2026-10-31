# Terraform AWS Infrastructure

## Project Overview

This project demonstrates how to provision AWS infrastructure using Terraform (Infrastructure as Code).

Instead of manually creating resources through the AWS Management Console, Terraform automates the infrastructure deployment using configuration files.

## Architecture

The project provisions the following AWS resources:

- VPC
- Public Subnet
- Internet Gateway
- Route Table
- Route Table Association
- Security Group
- EC2 Instance

## Technologies Used

- AWS
- Terraform
- AWS CLI
- Git & GitHub
- Kiro

## Deployment Steps

1. Configure AWS CLI credentials.
2. Initialize Terraform using `terraform init`.
3. Format configuration using `terraform fmt`.
4. Validate configuration using `terraform validate`.
5. Preview infrastructure using `terraform plan`.
6. Deploy resources using `terraform apply`.
7. Verify resources through AWS Console and Terraform outputs.

## Cleanup

To avoid unnecessary AWS charges, destroy the created infrastructure after testing:

```bash
terraform destroy
```

## Learning Outcomes

- Understanding Infrastructure as Code.
- Provisioning AWS resources using Terraform.
- Configuring VPC networking.
- Managing AWS infrastructure through Terraform.
- Understanding Terraform initialization, planning, deployment and destruction.

##
