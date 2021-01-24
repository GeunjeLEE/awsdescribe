output "ssm_pram_AWS_ACCESS_KEY_ID" {
    value = aws_ssm_parameter.AWS_ACCESS_KEY_ID.name
}

output "ssm_pram_AWS_SECRET_ACCESS_KEY" {
    value = aws_ssm_parameter.AWS_SECRET_ACCESS_KEY.name
}

output "ssm_pram_SECRET_KEY" {
    value = aws_ssm_parameter.SECRET_KEY.name
}

output "ssm_pram_DB_USER" {
    value = aws_ssm_parameter.DB_USER.name
}

output "ssm_pram_DB_PWD" {
    value = aws_ssm_parameter.DB_PWD.name
}