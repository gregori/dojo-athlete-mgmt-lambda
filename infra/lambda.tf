data "archive_file" "zip" {
  type        = "zip"
  source_file = "../app/lambda_function.py"
  output_path = "../app/lambda_function.zip"
}

resource "aws_lambda_function" "lambda_function" {
  filename         = data.archive_file.zip.output_path
  source_code_hash = data.archive_file.zip.output_base64sha256

  function_name = var.project_name
  role          = aws_iam_role.lambda_role.arn
  handler       = "lambda_function.lambda_handler"
  runtime       = "python3.12"
  timeout       = 10
  # publish       = true

  environment {
    variables = {
      S3_BUCKET = aws_s3_bucket.dojo_athlete.id
    }
  }
}

resource "aws_lambda_permission" "lambda_permission" {
  statement_id  = "AllowAPIGatewayInvoke"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.lambda_function.arn
  principal     = "apigateway.amazonaws.com"

  source_arn = "${aws_api_gateway_rest_api.api_gateway.execution_arn}/*/*"
}

#resource "aws_lambda_alias" "alias_dev" {
#  name             = "dev"
#  description      = "dev"
#  function_name    = aws_lambda_function.lambda_function.arn
#  function_version = "$LATEST"
#}
#
#resource "aws_lambda_alias" "alias_prod" {
#  name             = "prod"
#  description      = "prod"
#  function_name    = aws_lambda_function.lambda_function.arn
#  function_version = "$LATEST"
#}

#resource "aws_lambda_permission" "permission_dev" {
#  statement_id  = "AllowAPIGatewayInvoke"
#  action        = "lambda:InvokeFunction"
#  function_name = "${aws_lambda_function.lambda_function.function_name}:dev"
#  principal     = "apigateway.amazonaws.com"
#
#  # The "/*/*" portion grants access from any method on any resource
#  # within the API Gateway REST API.
#  source_arn = "${aws_api_gateway_rest_api.api_gateway.execution_arn}/*/GET/athletes"
#}
#
#resource "aws_lambda_permission" "permission_prod" {
#  statement_id  = "AllowAPIGatewayInvoke"
#  action        = "lambda:InvokeFunction"
#  function_name = "${aws_lambda_function.hello.function_name}:prod"
#  principal     = "apigateway.amazonaws.com"
#
#  # The "/*/*" portion grants access from any method on any resource
#  # within the API Gateway REST API.
#  source_arn = "${aws_api_gateway_rest_api.api_gateway.execution_arn}/*/GET/athletes"
#}
