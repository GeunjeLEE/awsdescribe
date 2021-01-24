resource "aws_ssm_parameter" "AWS_ACCESS_KEY_ID" {
  name        = "ACCESS_KEY_ID-${var.service}"
  description = "ACCESS_KEY_ID-${var.service}"
  type        = "SecureString"
  value       = "foo"
}

resource "aws_ssm_parameter" "AWS_SECRET_ACCESS_KEY" {
  name        = "SECRET_ACCESS_KEY-${var.service}"
  description = "SECRET_ACCESS_KEY-${var.service}"
  type        = "SecureString"
  value       = "foo"
}

resource "aws_ssm_parameter" "SECRET_KEY" {
  name        = "SECRET_KEY-${var.service}"
  description = "SECRET_KEY-${var.service}"
  type        = "SecureString"
  value       = "foo"
}

resource "aws_ssm_parameter" "DB_USER" {
  name        = "DB_USER-${var.service}"
  description = "DB_USER-${var.service}"
  type        = "SecureString"
  value       = "foo"
}

resource "aws_ssm_parameter" "DB_PWD" {
  name        = "DB_PWD-${var.service}"
  description = "DB_PWD-${var.service}"
  type        = "SecureString"
  value       = "foo"
}

