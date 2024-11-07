# VPC Configuration

# Create Application VPC
resource "aws_vpc" "main_vpc" {
  cidr_block = "10.0.0.0/16"
  enable_dns_support   = true
  enable_dns_hostnames = true
  tags = {
    Name    = "${var.app_prefix}-main-vpc"
    Project = var.app_name
  }
}

# Public Subnet for S3 Bucket and NAT Gateway
resource "aws_subnet" "public_subnet_1" {
  vpc_id     = aws_vpc.main_vpc.id
  cidr_block = "10.0.1.0/24"
  availability_zone = "ca-central-1a"
  map_public_ip_on_launch = true  # Assign public IPs to instances
  tags = {
    Name    = "${var.app_prefix}-public-subnet-1"
    Project = var.app_name
  }
}

# Public Subnet for Coverage Redundancy
resource "aws_subnet" "public_subnet_2" {
  vpc_id     = aws_vpc.main_vpc.id
  cidr_block = "10.0.3.0/24"
  availability_zone = "ca-central-1b"
  map_public_ip_on_launch = true
  tags = {
    Name    = "${var.app_prefix}-public-subnet-2"
    Project = var.app_name
  }
}

# Private Subnet for RDS & Lambda
resource "aws_subnet" "private_subnet_1" {
  vpc_id     = aws_vpc.main_vpc.id
  cidr_block = "10.0.2.0/24"
  availability_zone = "ca-central-1a"
  tags = {
    Name    = "${var.app_prefix}-private-subnet-1"
    Project = var.app_name
  }
}

# Private Subnet for Coverage Redundancy
resource "aws_subnet" "private_subnet_2" {
  vpc_id     = aws_vpc.main_vpc.id
  cidr_block = "10.0.4.0/24"
  availability_zone = "ca-central-1b"
  tags = {
    Name    = "${var.app_prefix}-private-subnet-2"
    Project = var.app_name
  }
}

# Internet Gateway for Public Internet Access
resource "aws_internet_gateway" "igw" {
  vpc_id = aws_vpc.main_vpc.id
  tags = {
    Name    = "${var.app_prefix}-main-igw"
    Project = var.app_name
  }
}

# NAT Gateway for Private Subnet Internet Access
resource "aws_eip" "nat_eip" {
  domain = "vpc"
  tags = {
    Name    = "${var.app_prefix}-nat-eip"
    Project = var.app_name
  }
}

resource "aws_nat_gateway" "nat_gateway" {
  allocation_id = aws_eip.nat_eip.id
  subnet_id     = aws_subnet.public_subnet_1.id  # NAT Gateway in public subnet
  tags = {
    Name    = "${var.app_prefix}-nat-gateway"
    Project = var.app_name
  }
}

# Route Table for Public Subnet (Internet access)
resource "aws_route_table" "public_route_table" {
  vpc_id = aws_vpc.main_vpc.id
  route {
    cidr_block = "0.0.0.0/0"  # Route all traffic to the internet
    gateway_id = aws_internet_gateway.igw.id
  }
  tags = {
    Name    = "${var.app_prefix}-public-route-table"
    Project = var.app_name
  }
}

# Route Table Association for Public Subnets
resource "aws_route_table_association" "public_route_table_assoc_1" {
  subnet_id      = aws_subnet.public_subnet_1.id
  route_table_id = aws_route_table.public_route_table.id
}

# Route Table Association for Public Subnets
resource "aws_route_table_association" "public_route_table_assoc_2" {
  subnet_id      = aws_subnet.public_subnet_2.id
  route_table_id = aws_route_table.public_route_table.id
}

# Route Table for Private Subnet
resource "aws_route_table" "private_route_table_1" {
  vpc_id = aws_vpc.main_vpc.id
  route {
    cidr_block     = "0.0.0.0/0"
    nat_gateway_id = aws_nat_gateway.nat_gateway.id
  }
  tags = {
    Name    = "${var.app_prefix}-private-route-table-1"
    Project = var.app_name
  }
}

# Route Table for Private Subnets
resource "aws_route_table" "private_route_table_2" {
  vpc_id = aws_vpc.main_vpc.id
  route {
    cidr_block     = "0.0.0.0/0"
    nat_gateway_id = aws_nat_gateway.nat_gateway.id
  }
  tags = {
    Name    = "${var.app_prefix}-private-route-table-2"
    Project = var.app_name
  }
}

# Route Table Association for Private Subnets
resource "aws_route_table_association" "private_route_table_assoc_1" {
  subnet_id      = aws_subnet.private_subnet_1.id
  route_table_id = aws_route_table.private_route_table_1.id
}

# Route Table Association for Private Subnets
resource "aws_route_table_association" "private_route_table_assoc_2" {
  subnet_id      = aws_subnet.private_subnet_2.id
  route_table_id = aws_route_table.private_route_table_2.id
}

# Subnet Group for RDS
resource "aws_db_subnet_group" "rds_subnet_group" {
  name       = "${var.app_prefix}-rds-subnet-group"
  subnet_ids = [aws_subnet.public_subnet_1.id, aws_subnet.public_subnet_2.id]
  tags = {
    Name    = "${var.app_prefix}-rds-subnet-group"
    Project = var.app_name
  }
}