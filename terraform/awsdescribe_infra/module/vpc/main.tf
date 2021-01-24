# Vpc
resource "aws_vpc" "this" {
  cidr_block       = "10.0.0.0/16"
  enable_dns_support     = true
  enable_dns_hostnames   = true

  tags = {
    Name = "vpc_${var.service}"
  }
}

# Public Subnet
resource "aws_subnet" "public_b" {
  vpc_id     = aws_vpc.this.id
  cidr_block = "10.0.0.0/24"
  availability_zone = "ap-northeast-1d"
  map_public_ip_on_launch = true 

  tags = {
    Name = "subnet_public_${var.service}_d"
  }
}

resource "aws_subnet" "public_c" {
  vpc_id     = aws_vpc.this.id
  cidr_block = "10.0.1.0/24"
  availability_zone = "ap-northeast-1c"
  map_public_ip_on_launch = true 

  tags = {
    Name = "subnet_public_${var.service}_c"
  }
}


# Private Subnet
resource "aws_subnet" "private_b" {
  vpc_id     = aws_vpc.this.id
  cidr_block = "10.0.2.0/24"
  availability_zone = "ap-northeast-1d"

  tags = {
    Name = "subnet_private_${var.service}_d"
  }
}

# Private Subnet
resource "aws_subnet" "private_c" {
  vpc_id     = aws_vpc.this.id
  cidr_block = "10.0.3.0/24"
  availability_zone = "ap-northeast-1c"

  tags = {
    Name = "subnet_private_${var.service}_c"
  }
}

# Internet Gateway
resource "aws_internet_gateway" "this" {
  vpc_id = aws_vpc.this.id

  tags = {
    Name = "igw_${var.service}"
  }
}

resource "aws_eip" "nat" {
  vpc = true

  tags = {
    Name = "nat_gateway_eip_${var.service}"
  }
}

# Nat Gateway
resource "aws_nat_gateway" "this" {
  allocation_id = aws_eip.nat.id
  subnet_id     = aws_subnet.public_b.id

  tags = {
    Name = "ngw_${var.service}"
  }
}

# Public Route table
resource "aws_default_route_table" "this" {
  default_route_table_id = aws_vpc.this.default_route_table_id

  route {
    cidr_block = "0.0.0.0/0"
    gateway_id = aws_internet_gateway.this.id
  }

  tags = {
    Name = "public_route_table_${var.service}"
  }
}

# Private Route table
resource "aws_route_table" "this" {
  vpc_id  = aws_vpc.this.id

  route {
    cidr_block = "0.0.0.0/0"
    gateway_id = aws_nat_gateway.this.id
  }

  tags = {
    Name = "private_route_table_${var.service}"
  }

  lifecycle {
    ignore_changes = ["*"]
  }
}

# route table associate
resource "aws_route_table_association" "public_b" {
  subnet_id      = aws_subnet.public_b.id
  route_table_id = aws_default_route_table.this.id
}

resource "aws_route_table_association" "public_c" {
  subnet_id      = aws_subnet.public_c.id
  route_table_id = aws_default_route_table.this.id
}


# route table associate
resource "aws_route_table_association" "private_b" {
  subnet_id      = aws_subnet.private_b.id
  route_table_id = aws_route_table.this.id
}

# route table associate
resource "aws_route_table_association" "private_c" {
  subnet_id      = aws_subnet.private_c.id
  route_table_id = aws_route_table.this.id
}

