terraform {
  required_version = ">= 0.13"

  required_providers {
    aws = {
      source = "hashicorp/aws"
    }
  }

  backend "s3" {
    bucket = "s3 bucket"
    key    = "path/to/state.file"
    region = "ap-northeast-1"
  }
}

data "terraform_remote_state" "ssm" {
  backend = "s3"

  config = {
    bucket = "s3 bucket"
    key    = "path/to/state.file"
    region = "ap-northeast-1"
  }
}
