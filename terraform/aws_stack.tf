#Create s3 bucket
resource "aws_s3_bucket" "daily-transaction-data" {
  bucket = "joy-skincare-daily-transaction-data"

  tags = {
    Name        = "Joy"
    Environment = "Production"
  }
}


# # Create SSM parameter

# resource "aws_ssm_parameter" "access-key" {
#   name  = "joy_access_key"
#   type  = "String"
#   value = aws_iam_access_key.access-key.id
# }

# resource "aws_ssm_parameter" "secret-key" {
#   name  = "joy_secret_key"
#   type  = "String"
#   value = aws_iam_access_key.access-key.secret
# }
# /