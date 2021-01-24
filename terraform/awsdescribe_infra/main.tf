locals {
    service             = "awsdescribe"
}

module "vpc" {
    source              = "./module/vpc"
    service             = local.service
}

module "ecr" {
    source              = "./module/ecr"
    service             = local.service
}

module "backends-host" {
    source              = "./module/ec2"
    vpc_id              = module.vpc.vpc_id
    subnet_id           = module.vpc.private_subnet_c_id
    service             = local.service
}

module "alb" {
    source              = "./module/alb"
    vpc_id              = module.vpc.vpc_id
    subnets             = [module.vpc.public_subnet_d_id,module.vpc.public_subnet_c_id]
    service             = local.service
}

module "ecs" {
    source              = "./module/ecs"
    vpc_id              = module.vpc.vpc_id
    subnets             = [module.vpc.private_subnet_d_id,module.vpc.private_subnet_c_id]
    alb_sg              = module.alb.alb_sg_id
    lb_target_group     = module.alb.alb_target_arn
    service             = local.service
    container_df_env_values  = {
        "DB_NAME"                   = "awsdescribe"
        "DB_HOST"                   = "10.0.3.190"
        "BROKER_URL"                = "redis://127.0.0.1:6379/0"
    }
    container_df_env_secret_values = {
        "AWS_ACCESS_KEY_ID"         = data.terraform_remote_state.ssm.outputs.ssm_pram_AWS_ACCESS_KEY_ID
        "AWS_SECRET_ACCESS_KEY"     = data.terraform_remote_state.ssm.outputs.ssm_pram_AWS_SECRET_ACCESS_KEY
        "SECRET_KEY"                = data.terraform_remote_state.ssm.outputs.ssm_pram_SECRET_KEY
        "DB_USER"                   = data.terraform_remote_state.ssm.outputs.ssm_pram_DB_USER
        "DB_PWD"                    = data.terraform_remote_state.ssm.outputs.ssm_pram_DB_PWD
    }
}