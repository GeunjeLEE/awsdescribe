output "vpc_id" {
    value = aws_vpc.this.id
}

output "public_subnet_d_id" {
    value = aws_subnet.public_d.id
}

output "public_subnet_c_id" {
    value = aws_subnet.public_c.id
}

output "private_subnet_d_id" {
    value = aws_subnet.private_d.id
}

output "private_subnet_c_id" {
    value = aws_subnet.private_c.id
}