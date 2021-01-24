resource "aws_instance" "this" {
    ami                    = "ami-01748a72bed07727c"
    vpc_security_group_ids = [aws_security_group.this.id]
    subnet_id              = var.subnet_id
    instance_type          = "t2.small"
    iam_instance_profile   = aws_iam_role.this.name

    tags = {
        Name = "${var.service}-backend-host"
    }
}

resource "aws_iam_instance_profile" "this" {
    name = "${var.service}_ssm_role"
    role = aws_iam_role.this.name
}

resource "aws_iam_role" "this" {
    name = "${var.service}_ssm_role"

    assume_role_policy = <<EOF
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Action": "sts:AssumeRole",
            "Principal": {
               "Service": "ec2.amazonaws.com"
            },
            "Effect": "Allow",
            "Sid": ""
        }
    ]
}
EOF
}

resource "aws_iam_role_policy_attachment" "this" {
    role       = aws_iam_role.this.name
    policy_arn = "arn:aws:iam::aws:policy/AmazonSSMManagedInstanceCore"
}

resource "aws_security_group" "this" {
  name        = "${var.service}-backends-sg"
  description = "Allow 3306 inbound traffic"
  vpc_id      = var.vpc_id

  ingress {
    description = "mysql port"
    from_port   = 3306
    to_port     = 3306
    protocol    = "tcp"
    cidr_blocks = ["10.0.0.0/16"]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

}
