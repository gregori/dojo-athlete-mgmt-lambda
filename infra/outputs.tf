output "s3_bucket_name" {
  description = "Nome do bucket S3"
  value       = aws_s3_bucket.dojo_athlete.id
}


output "lambda_arn" {
  description = "ARN da função Lambda"
  value       = [
    aws_lambda_function.lambda_function.arn
  ]
}
