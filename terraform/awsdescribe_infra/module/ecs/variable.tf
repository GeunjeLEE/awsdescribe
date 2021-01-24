variable "vpc_id" {
    default = ""
}

variable "subnets" {
    type    = list(string)
    default = []
}

variable "lb_target_group" {
    default = ""
}

variable "alb_sg" {
    default = ""
}

variable "service" {
    default = ""
}

variable "container_df_env_values" {
  type    = map(string)
  default = {}
}

variable "container_df_env_secret_values" {
  type    = map(string)
  default = {}
}


