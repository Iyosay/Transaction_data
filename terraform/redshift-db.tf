
# REDSHIFT SUBNET GROUP
resource "aws_redshift_subnet_group" "transactiondata_subnet_group" {
  name = "transactiondata-subnet-group"
  subnet_ids = [
    aws_subnet.public_sub.id,
    aws_subnet.private_sub.id
  ]


 tags = {
    Name        = "transactiondata-subnet-group"
    Environment = "dev"
 
 }

}

resource "random_password" "mypassword" {
  length  = 20
  special = false
}

resource "aws_ssm_parameter" "redshift_database_password" {
  name  = "redshift-database-password"
  type  = "String"
  value = random_password.mypassword.result

}

# REDSHFIT CLUSTER
resource "aws_redshift_cluster" "transactiondata_redshift_cluster" {
  cluster_identifier        = "redshift-cluster"
  database_name             = "transactiondata_db"
  master_username           = "admin"
  master_password           = aws_ssm_parameter.redshift_database_password.value
  node_type                 = "ra3.large"
  cluster_type              = "multi-node"
  iam_roles                 = [aws_iam_role.transactiondata_redshift_role.arn]
  number_of_nodes           = 2
  publicly_accessible       = true
  cluster_subnet_group_name = aws_redshift_subnet_group.transactiondata_subnet_group.name
  vpc_security_group_ids    = [aws_security_group.transactiondata_redshift_sg.id]


  tags = {
    Name        = "redshift-cluster"
    Environment = "dev"
    Owner       = "joy"
  }

}


# IAM ROLE FOR REDSHIFT

resource "aws_iam_role" "transactiondata_redshift_role" {
  name = "transcdata-redshift-role"

  # Terraform's "jsonencode" function converts a
  # Terraform expression result to valid JSON syntax.
  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = "sts:AssumeRole"
        Effect = "Allow"
        Sid    = ""
        Principal = {
          Service = "redshift.amazonaws.com"
        }
      },
    ]
  })
}

resource "aws_iam_role_policy" "transactiondata_redshift_policy" {
  name = "transacdata_policy"
  role = aws_iam_role.transactiondata_redshift_role.id

  policy = jsonencode({
    Version = "2012-10-17",
    Statement = [
      {
        Effect = "Allow",
        Action = [
          "s3:GetObject",
          "s3:PutObject"
        ],
        Resource = "arn:aws:s3:::joy_skincare_daily_transaction_data/*"
      },
      {
        Effect = "Allow",
        Action = [
          "s3:ListBucket"
        ],
        Resource = "arn:aws:s3:::joy_skincare_daily_transaction_data"
      }
    ]
  })
}
