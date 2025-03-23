#
# lambda assume role policy
#
resource "aws_iam_role" "lambda_role" {
  name        = "${var.project_name}-role"
  description = "${var.project_desc} Policy"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = "sts:AssumeRole"
        Effect = "Allow"
        Principal = {
          Service = "lambda.amazonaws.com"
        }
      },
    ]
  })
}

resource "aws_iam_policy" "lambda_policy" {
  name        = "${var.project_name}-policy"
  description = "${var.project_desc} Policy"

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = [
          "ec2:Describe*",
        ]
        Effect   = "Allow"
        Resource = "*"
      },
    ]
  },{
    Version = "2012-10-17"
    Statement = [
      {
        Action = [
          "s3:ListBucket",
          "s3:PutObject",
          "s3:GetObject"
        ]
        Effect   = "Allow"
        Resource = [
          "${aws_s3_bucket.dojo_athlete.arn}",
          "${aws_s3_bucket.dojo_athlete.arn}/*"
        ]
      },
    ]
  },{
    Version = "2012-10-17"
    Statement = [
      {
        Action = [
          "lambda:InvokeFunction"
        ]
        Effect   = "Allow"
        Resource = "*"
      },
    ]
  })
}

resource "aws_iam_role_policy_attachment" "role-policy-attachment" {
  policy_arn = aws_iam_policy.lambda_policy.arn
  role       = aws_iam_role.lambda_role.id
}