
# VPC
resource "aws_vpc" "transactiondata_vpc" {
  cidr_block = "10.10.0.0/16"

  tags = {
    Name = "transactiondata-vpc"
  }
}

# IGW
resource "aws_internet_gateway" "igw" {
  vpc_id = aws_vpc.transactiondata_vpc.id

  tags = {
    Name = "transactiondata-igw"
  }
}

## PUBLIC SUBNET
resource "aws_subnet" "public_sub" {
  vpc_id                  = aws_vpc.transactiondata_vpc.id
  cidr_block              = "10.10.0.0/24"
  availability_zone       = "eu-west-2a"
  map_public_ip_on_launch = true # Give public ip

  tags = {
    Name = "transactiondata_public_sub"
  }
}


resource "aws_route_table_association" "public_rt_a" {
  subnet_id      = aws_subnet.public_sub.id
  route_table_id = aws_route_table.redshift_rt.id
}

## PRIVATE SUBNET
resource "aws_subnet" "private_sub" {
  vpc_id            = aws_vpc.transactiondata_vpc.id
  cidr_block        = "10.10.1.0/24"
  availability_zone = "eu-west-2b" # This is another availability zone for resilience

  tags = {
    Name = "redshift_private_sub"
  }
}

resource "aws_route_table" "redshift_rt" {
  vpc_id = aws_vpc.transactiondata_vpc.id


  tags = {
    Name = "redshift_priv_rt"
  }
}


resource "aws_route" "transactiondata_redshift_route" {
  route_table_id         = aws_route_table.redshift_rt.id
  destination_cidr_block = "0.0.0.0/0"
  gateway_id             = aws_internet_gateway.igw.id
}


resource "aws_route_table_association" "private_rt_a" {
  subnet_id      = aws_subnet.private_sub.id
  route_table_id = aws_route_table.redshift_rt.id
}



## SECURITY GROUP
resource "aws_security_group" "transactiondata_redshift_sg" {
  name        = "allow_traffic"
  description = "Allow inbound traffic and outbound"
  vpc_id      = aws_vpc.transactiondata_vpc.id

  tags = {
    Name = "transactiondata_redshift_sg"
  }
}

resource "aws_vpc_security_group_ingress_rule" "ingress_rule" {
  security_group_id = aws_security_group.transactiondata_redshift_sg.id
  cidr_ipv4         = "0.0.0.0/0"
  from_port         = 5439
  to_port           = 5439
  ip_protocol       = "tcp"
  
}

resource "aws_vpc_security_group_egress_rule" "egress_rule" {
  security_group_id = aws_security_group.transactiondata_redshift_sg.id
  cidr_ipv4         = "0.0.0.0/0"
  ip_protocol       = "-1" # semantically equivalent to all ports,allow all types of ip-protocol
}

