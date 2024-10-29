# Frontend Configuration - S3 Bucket & CloudFront

# Create S3 Bucket for Frontend
resource "aws_s3_bucket" "frontend_bucket" {
  bucket = "${var.app_prefix}-frontend-bucket"

  tags = {
    Name    = "${var.app_prefix}-frontend-bucket"
    Project = var.app_name
  }
}

# Specify Private S3 Bucket Access Control Policy
resource "aws_s3_bucket_acl" "frontend_bucket_acl" {
  bucket = aws_s3_bucket.frontend_bucket.id
  acl = "private"
}

# Enable Versioning on the S3 Bucket
resource "aws_s3_bucket_versioning" "frontend_bucket_versioning" {
  bucket = aws_s3_bucket.frontend_bucket.id
  versioning_configuration {
    status = "Enabled"
  }
}

# Create OAI for Frontend Bucket
resource "aws_cloudfront_origin_access_identity" "oai" {
  comment = "OAI for secure S3 access"
}

# Create Policy to Allow OAI Access Frontend S3 Bucket
resource "aws_s3_bucket_policy" "frontend_policy" {
  bucket = aws_s3_bucket.frontend_bucket.id

  policy = jsonencode({
    "Version": "2012-10-17",
    "Statement": [
      {
        "Effect": "Allow",
        "Principal": {
          "AWS": aws_cloudfront_origin_access_identity.oai.iam_arn  # Allow OAI-verified Access
        },
        "Action": "s3:GetObject",
        "Resource": "${aws_s3_bucket.frontend_bucket.arn}/*" # Access is to frontend bucket resource
      }
    ]
  })
}

# Create CloudFront Web Distribution to Route User Request
resource "aws_cloudfront_distribution" "cdn" {
  origin {
    domain_name = aws_s3_bucket.frontend_bucket.bucket_regional_domain_name
    origin_id   = "S3-Frontend"

    s3_origin_config {
      origin_access_identity = aws_cloudfront_origin_access_identity.oai.cloudfront_access_identity_path
    }
  }

  restrictions {
    geo_restriction {
      restriction_type = "none" # Do not restrict distribution based on Geo
    }
  }

  enabled             = true
  default_root_object = "index.html"

  default_cache_behavior {
    allowed_methods        = ["GET", "HEAD"]
    cached_methods         = ["GET", "HEAD"]
    target_origin_id       = "S3-Frontend"
    forwarded_values {
      query_string = false
      cookies {
        forward = "none"
      }
    }
    viewer_protocol_policy = "redirect-to-https"
  }

  viewer_certificate {
    cloudfront_default_certificate = true
  }

  tags = {
    Name    = "${var.app_prefix}-frontend-distribution"
    Project = var.app_name
  }
}