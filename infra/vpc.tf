# VPC definition
resource "aws_vpc" "web_app_vpc" {
  cidr_block = "10.0.0.0/16" # "10.0.0.0/16"
  enable_dns_support   = true
  enable_dns_hostnames = true
  tags = {
    Name = "${var.application_name}-vpc"
  }
}

# Public Subnet
resource "aws_subnet" "public_subnet_1" {
  vpc_id     = aws_vpc.web_app_vpc.id
  cidr_block = "10.0.1.0/24"
  availability_zone = "ca-central-1a"
  map_public_ip_on_launch = true  # Assign public IPs to instances
  tags = {
    Name = "${var.application_name}-public-subnet-1"
  }
}

# Public Subnet
resource "aws_subnet" "public_subnet_2" {
  vpc_id     = aws_vpc.web_app_vpc.id
  cidr_block = "10.0.3.0/24"
  availability_zone = "ca-central-1b"
  tags = {
    Name = "${var.application_name}-public-subnet-2"
  }
}

# Private Subnet
resource "aws_subnet" "private_subnet_1" {
  vpc_id     = aws_vpc.web_app_vpc.id
  cidr_block = "10.0.2.0/24"
  availability_zone = "ca-central-1a"
  tags = {
    Name = "${var.application_name}-private-subnet-1"
  }
}

# Private Subnet
resource "aws_subnet" "private_subnet_2" {
  vpc_id     = aws_vpc.web_app_vpc.id
  cidr_block = "10.0.4.0/24"
  availability_zone = "ca-central-1b"
  tags = {
    Name = "${var.application_name}-private-subnet-2"
  }
}

# Internet Gateway (to allow public access to the frontend)
resource "aws_internet_gateway" "igw" {
  vpc_id = aws_vpc.web_app_vpc.id
  tags = {
    Name = "${var.application_name}-igw"
  }
}

# NAT Gateway (to allow outbound internet access for private subnet)
resource "aws_eip" "nat_eip" {
  domain = "vpc"
  tags = {
    Name = "${var.application_name}-nat-eip"
  }
}

resource "aws_nat_gateway" "nat_gateway" {
  allocation_id = aws_eip.nat_eip.id
  subnet_id     = aws_subnet.public_subnet_1.id  # NAT Gateway in public subnet
  tags = {
    Name = "${var.application_name}-nat-gateway"
  }
}

# Route Table for Public Subnet (Internet access)
resource "aws_route_table" "public_route_table" {
  vpc_id = aws_vpc.web_app_vpc.id
  route {
    cidr_block = "0.0.0.0/0"  # Route all traffic to the internet
    gateway_id = aws_internet_gateway.igw.id
  }
  tags = {
    Name = "${var.application_name}-public-route-table"
  }
}

# Route Table Association for Public Subnet
resource "aws_route_table_association" "public_route_table_assoc_1" {
  subnet_id      = aws_subnet.public_subnet_1.id
  route_table_id = aws_route_table.public_route_table.id
}

# Route Table Association for Public Subnet
resource "aws_route_table_association" "public_route_table_assoc_2" {
  subnet_id      = aws_subnet.public_subnet_2.id
  route_table_id = aws_route_table.public_route_table.id
}

# Route Table for Private Subnet (NAT Gateway for outbound traffic)
resource "aws_route_table" "private_route_table" {
  vpc_id = aws_vpc.web_app_vpc.id
  route {
    cidr_block     = "0.0.0.0/0"
    nat_gateway_id = aws_nat_gateway.nat_gateway.id
  }
  tags = {
    Name = "${var.application_name}-private-route-table"
  }
}

# Route Table Association for Private Subnet
resource "aws_route_table_association" "private_route_table_assoc_1" {
  subnet_id      = aws_subnet.private_subnet_1.id
  route_table_id = aws_route_table.private_route_table.id
}

# Route Table Association for Private Subnet
resource "aws_route_table_association" "private_route_table_assoc_2" {
  subnet_id      = aws_subnet.private_subnet_2.id
  route_table_id = aws_route_table.private_route_table.id
}

# Subnet Group for RDS
resource "aws_db_subnet_group" "rds_subnet_group" {
  name       = "rds-subnet-group"
  subnet_ids = [aws_subnet.public_subnet_1.id, aws_subnet.public_subnet_2.id, aws_subnet.private_subnet_1.id,
    aws_subnet.private_subnet_2.id]
  tags = {
    Name = "${var.application_name}-rds-subnet-group"
  }
}