terraform {
  required_version = ">= 0.13"

  required_providers {
    aws = {
      source = "hashicorp/aws"
    }
  }

  backend "s3" {
    bucket = "s3_bucket_name"
    key    = "path/to/state_file"
    region = "ap-northeast-1"
  }
}
