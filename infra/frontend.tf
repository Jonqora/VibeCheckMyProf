# TODO: Work with Frontend to Finish Configuration

# Create S3 bucket for front end
resource "aws_s3_bucket" "frontend_bucket" {
  bucket = "my-frontend-bucket"  # Change to a unique name

  tags = {
    Name = "Frontend Hosting Bucket"
    Environment = "Production"
  }
}

# Enable static website hosting
resource "aws_s3_bucket_website_configuration" "bucket_website_config" {
  bucket = aws_s3_bucket.frontend_bucket.id

  index_document {
    suffix = "index.html"
  }

  error_document {
    key = "error.html"
  }
}

# Configure a bucket policy to make it publicly accessible
resource "aws_s3_bucket_policy" "frontend_bucket_policy" {
  bucket = aws_s3_bucket.frontend_bucket.id

  policy = jsonencode({
    "Version": "2012-10-17",
    "Statement": [
      {
        "Effect": "Allow",
        "Principal": "*",
        "Action": "s3:GetObject",
        "Resource": "${aws_s3_bucket.frontend_bucket.arn}/*"
      }
    ]
  })
}
