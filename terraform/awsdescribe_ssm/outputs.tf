# https://www.terraform.io/docs/providers/terraform/d/remote_state.html#root-outputs-only
# Only the root-level output values from the remote state snapshot are exposed for use elsewhere in your module. 

output "ssm_pram_AWS_ACCESS_KEY_ID" {
    value = module.ssm.ssm_pram_AWS_ACCESS_KEY_ID
}

output "ssm_pram_AWS_SECRET_ACCESS_KEY" {
    value = module.ssm.ssm_pram_AWS_SECRET_ACCESS_KEY
}

output "ssm_pram_SECRET_KEY" {
    value = module.ssm.ssm_pram_SECRET_KEY
}

output "ssm_pram_DB_USER" {
    value = module.ssm.ssm_pram_DB_USER
}

output "ssm_pram_DB_PWD" {
    value = module.ssm.ssm_pram_DB_PWD
}