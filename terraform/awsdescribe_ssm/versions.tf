terraform {
  required_version = ">= 0.13"

  required_providers {
    aws = {
      source = "hashicorp/aws"
    }
  }

  backend "s3" {
    bucket = "aws-describe-terraform-log"
    key    = "ssm/terraform.tfstate"
    region = "ap-northeast-1"
  }
}
