resource "aws_api_gateway_rest_api" "api_gateway" {
  name        = "${var.project_name}-API"
  description = "${var.project_desc} API"
}

## rote /aulas
resource "aws_api_gateway_resource" "aulas" {
  rest_api_id = aws_api_gateway_rest_api.api_gateway.id
  parent_id   = aws_api_gateway_rest_api.api_gateway.root_resource_id
  path_part   = "aulas"
}

resource "aws_api_gateway_method" "aulas_post" {
  rest_api_id   = aws_api_gateway_rest_api.api_gateway.id
  resource_id   = aws_api_gateway_resource.aulas.id
  http_method   = "POST"
  authorization = "NONE"
}

resource "aws_api_gateway_integration" "aulas_integration" {
  rest_api_id = aws_api_gateway_rest_api.api_gateway.id
  resource_id = aws_api_gateway_resource.aulas.id
  http_method = aws_api_gateway_method.aulas_post.http_method
  integration_http_method = "POST"
  type = "AWS_PROXY"
  uri = aws_lambda_function.lambda_function.invoke_arn
}

## rote /checkin
resource "aws_api_gateway_resource" "checkin" {
  rest_api_id = aws_api_gateway_rest_api.api_gateway.id
  parent_id   = aws_api_gateway_rest_api.api_gateway.root_resource_id
  path_part   = "checkin"
}

resource "aws_api_gateway_method" "checkin_post" {
  rest_api_id   = aws_api_gateway_rest_api.api_gateway.id
  resource_id   = aws_api_gateway_resource.checkin.id
  http_method   = "POST"
  authorization = "NONE"
}

resource "aws_api_gateway_integration" "checkin_integration" {
  rest_api_id = aws_api_gateway_rest_api.api_gateway.id
  resource_id = aws_api_gateway_resource.checkin.id
  http_method = aws_api_gateway_method.checkin_post.http_method
  integration_http_method = "POST"
  type = "AWS_PROXY"
  uri = aws_lambda_function.lambda_function.invoke_arn
}

## rote /presencas
resource "aws_api_gateway_resource" "presencas" {
  rest_api_id = aws_api_gateway_rest_api.api_gateway.id
  parent_id   = aws_api_gateway_rest_api.api_gateway.root_resource_id
  path_part   = "presencas"
}

resource "aws_api_gateway_method" "presencas_get" {
  rest_api_id   = aws_api_gateway_rest_api.api_gateway.id
  resource_id   = aws_api_gateway_resource.presencas.id
  http_method   = "GET"
  authorization = "NONE"
}

resource "aws_api_gateway_integration" "presencas_integration" {
  rest_api_id = aws_api_gateway_rest_api.api_gateway.id
  resource_id = aws_api_gateway_resource.presencas.id
  http_method = aws_api_gateway_method.presencas_get.http_method
  integration_http_method = "POST"
  type = "AWS_PROXY"
  uri = aws_lambda_function.lambda_function.invoke_arn
}


resource "aws_api_gateway_deployment" "api_gateway_deployment" {
  depends_on  = [aws_api_gateway_method.aulas_post, aws_api_gateway_method.checkin_post, aws_api_gateway_method.presencas_get]
  rest_api_id = aws_api_gateway_rest_api.api_gateway.id
#  stage_name  = "prod"
}

resource "aws_api_gateway_stage" "stage" {
  deployment_id = aws_api_gateway_deployment.api_gateway_deployment.id
  rest_api_id   = aws_api_gateway_rest_api.api_gateway.id
  stage_name    = "dev"
}

resource "aws_api_gateway_method_settings" "example" {
  rest_api_id = aws_api_gateway_rest_api.api_gateway.id
  stage_name  = aws_api_gateway_stage.stage.stage_name
  method_path = "*/*"

  settings {
    metrics_enabled = true
    logging_level   = "INFO"
  }
}

resource "aws_api_gateway_account" "account" {
  cloudwatch_role_arn = aws_iam_role.api_gateway_role.arn
}