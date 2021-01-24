variable "vpc_id" {
    default = ""
}

variable "subnets" {
    type    = list(string)
    default = []
}

variable "service" {
    default = ""
}