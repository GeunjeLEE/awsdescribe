resource "aws_lb" "this" {
  name               = "${var.service}-alb"
  internal           = false
  load_balancer_type = "application"
  security_groups    = [aws_security_group.this.id]
  subnets            = var.subnets

  enable_deletion_protection = false
}

resource "aws_lb_listener" "this" {
  load_balancer_arn = aws_lb.this.arn
  port              = 80
  protocol          = "HTTP"

  default_action {
    type             = "forward"
    target_group_arn = aws_lb_target_group.this.arn
  }
}

resource "aws_lb_target_group" "this" {
  name        = "${var.service}-tg"
  port        = 80
  protocol    = "HTTP"
  vpc_id      = var.vpc_id
  target_type = "ip"

  health_check {
    interval            = 10
    healthy_threshold   = 3
    unhealthy_threshold = 3
    protocol            = "HTTP"
    port                = "traffic-port"
  }
}

resource "aws_security_group" "this" {
  name        = "${var.service}-for-alb"
  description = "Allow 80 inbound traffic"
  vpc_id      = var.vpc_id

  ingress {
    description = "http port"
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["13.114.248.99/32"]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}
