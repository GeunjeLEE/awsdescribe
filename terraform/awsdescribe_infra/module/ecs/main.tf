resource "aws_iam_role" "this" {
    name = "${var.service}_ecsTaskExecutionRole"

    assume_role_policy = <<EOF
{
  "Version": "2008-10-17",
  "Statement": [
    {
      "Sid": "",
      "Effect": "Allow",
      "Principal": {
        "Service": "ecs-tasks.amazonaws.com"
      },
      "Action": "sts:AssumeRole"
    }
  ]
}
EOF
}

resource "aws_iam_role_policy_attachment" "this" {
    role       = aws_iam_role.this.name
    policy_arn = aws_iam_policy.this.arn
}

resource "aws_iam_policy" "this" {
  name        = "${var.service}_ecsTaskExecutionPolicy"
  path        = "/"
  description = "${var.service}_ecsTaskExecutionPolicy"

  policy = <<EOF
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                "ecr:GetAuthorizationToken",
                "ecr:BatchCheckLayerAvailability",
                "ecr:GetDownloadUrlForLayer",
                "ecr:BatchGetImage",
                "logs:CreateLogStream",
                "logs:PutLogEvents",
                "ssm:GetParameters"
            ],
            "Resource": "*"
        }
    ]
}
EOF
}

resource "aws_ecs_cluster" "this" {
  name = "${var.service}-cluster"
}

data "template_file" "this" {
  template = file("./container-definitions/awsdescribe.json.tpl")

  vars = {
    container_df_env_values        = jsonencode([for k, v in var.container_df_env_values : { name = k, value = v }])
    container_df_env_secret_values = jsonencode([for k, v in var.container_df_env_secret_values : { name = k, valueFrom = v }])
  }
}

resource "aws_ecs_task_definition" "this" {
  family                      = "${var.service}_service"
  container_definitions       = data.template_file.this.rendered
  task_role_arn               = aws_iam_role.this.arn
  execution_role_arn          = aws_iam_role.this.arn
  network_mode                = "awsvpc"
  requires_compatibilities    = ["FARGATE"]
  cpu                         = 1024
  memory                      = 2048
}

resource "aws_ecs_service" "this" {
  name              = "${var.service}-service"
  cluster           = aws_ecs_cluster.this.id
  task_definition   = aws_ecs_task_definition.this.arn
  desired_count     = 1
  launch_type       = "FARGATE"

  network_configuration {
    subnets         = var.subnets
    security_groups = [aws_security_group.this.id]
  }

  load_balancer {
    target_group_arn = var.lb_target_group
    container_name   = "dajngo"
    container_port   = 8000
  }
}

resource "aws_security_group" "this" {
  name        = "${var.service}-sg-for-ecs"
  description = "Allow ecs inbound traffic"
  vpc_id      = var.vpc_id

  ingress {
    description = "all"
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    security_groups = [var.alb_sg]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

}

