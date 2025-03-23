resource "aws_s3_bucket" "dojo_athlete" {
  bucket = "${var.project_name}"
}

resource "aws_s3_bucket_ownership_controls" "this" {
  bucket = aws_s3_bucket.dojo_athlete.id

  rule {
    object_ownership = "ObjectWriter"
  }
}

resource "aws_s3_bucket_public_access_block" "this" {
  bucket = aws_s3_bucket.dojo_athlete.id

  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true
}

resource "aws_s3_bucket_server_side_encryption_configuration" "this" {
  bucket = aws_s3_bucket.dojo_athlete.id

  rule {
    apply_server_side_encryption_by_default {
      sse_algorithm     = "AES256"
    }
  }
}

data "aws_canonical_user_id" "current" {}

resource "aws_s3_bucket_acl" "this" {
  depends_on = [aws_s3_bucket_ownership_controls.this]

  bucket = aws_s3_bucket.dojo_athlete.id
  access_control_policy {
    grant {
      grantee {
        id   = data.aws_canonical_user_id.current.id
        type = "CanonicalUser"
      }
      permission = "FULL_CONTROL"
    }

    owner {
      id = data.aws_canonical_user_id.current.id
    }
  }
}

resource "aws_s3_bucket_versioning" "example" {
  bucket = aws_s3_bucket.dojo_athlete.id

  versioning_configuration {
    status = "Suspended"
  }
}
