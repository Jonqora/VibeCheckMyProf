# VPC Configuration

# Create Application VPC
resource "aws_vpc" "main_vpc" {
  cidr_block = "10.0.0.0/16"

  tags = {
    Name    = "main-vpc"
    Project = var.application_name
  }
}

# Public Subnet for S3 Bucket and NAT Gateway
resource "aws_subnet" "public_subnet_1" {
  vpc_id     = aws_vpc.main_vpc.id
  cidr_block = "10.0.1.0/24"
  availability_zone = "ca-central-1a"
  map_public_ip_on_launch = true  # Assign public IPs to instances
  tags = {
    Name    = "public-subnet-1"
    Project = var.application_name
  }
}

# Public Subnet for Coverage Redundancy
resource "aws_subnet" "public_subnet_2" {
  vpc_id     = aws_vpc.main_vpc.id
  cidr_block = "10.0.3.0/24"
  availability_zone = "ca-central-1b"
  tags = {
    Name    = "public-subnet-2"
    Project = var.application_name
  }
}

# Private Subnet for RDS & Lambda
resource "aws_subnet" "private_subnet_1" {
  vpc_id     = aws_vpc.main_vpc.id
  cidr_block = "10.0.2.0/24"
  availability_zone = "ca-central-1a"
  tags = {
    Name    = "private-subnet-1"
    Project = var.application_name
  }
}

# Private Subnet for Coverage Redundancy
resource "aws_subnet" "private_subnet_2" {
  vpc_id     = aws_vpc.main_vpc.id
  cidr_block = "10.0.4.0/24"
  availability_zone = "ca-central-1b"
  tags = {
    Name    = "private-subnet-2"
    Project = var.application_name
  }
}

# Internet Gateway for Public Internet Access
resource "aws_internet_gateway" "igw" {
  vpc_id = aws_vpc.main_vpc.id
  tags = {
    Name    = "main-igw"
    Project = var.application_name
  }
}

# NAT Gateway for Private Subnet Internet Access
resource "aws_eip" "nat_eip" {
  domain = "vpc"
  tags = {
    Name    = "nat-eip"
    Project = var.application_name
  }
}

resource "aws_nat_gateway" "nat_gateway" {
  allocation_id = aws_eip.nat_eip.id
  subnet_id     = aws_subnet.public_subnet_1.id  # NAT Gateway in public subnet
  tags = {
    Name    = "nat-gateway"
    Project = var.application_name
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
    Name    = "public-route-table"
    Project = var.application_name
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

# Route Table for Private Subnets
resource "aws_route_table" "private_route_table" {
  vpc_id = aws_vpc.main_vpc.id
  route {
    cidr_block     = "0.0.0.0/0"
    nat_gateway_id = aws_nat_gateway.nat_gateway.id
  }
  tags = {
    Name    = "private-route-table"
    Project = var.application_name
  }
}

# Route Table Association for Private Subnets
resource "aws_route_table_association" "private_route_table_assoc_1" {
  subnet_id      = aws_subnet.private_subnet_1.id
  route_table_id = aws_route_table.private_route_table.id
}

# Route Table Association for Private Subnets
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
    Name    = "rds-subnet-group"
    Project = var.application_name
  }
}