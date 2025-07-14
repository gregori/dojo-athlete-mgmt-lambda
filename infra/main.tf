terraform {
  backend "s3" {
    bucket   = "dojo-management-tfstate"
    key      = "dojo-lambda/dojo-athlete-mgmt-tfstate" ########
    region   = "sa-east-1"
    encrypt  = true
    skip_region_validation      = true
    skip_credentials_validation = true
    skip_metadata_api_check     = true
  }
}

variable "redeploy_token" {
  type    = string
  default = ""
}

module "lambda" {
  source = "git::https://github.com/DojoManagement/dojo-tf-modules.git//dojo-lambda?ref=fix--create-one-api-gw-resource-by-path_part"

  lambda_name     = "dojo-athlete-mgmt"
  source_dir      = "../lambda_build"
  handler         = "lambda_function.lambda_handler"
  runtime_version = "python3.12"
  access_s3       = true
  env             = "stg"
  app_version     = "v0.0.1"
  
  routes = {
    athletes        = ["POST", "GET"]
    "athletes/{id}" = ["GET", "PUT", "DELETE"]
  }
}

module "apigw_deployment" {
  source = "git::https://github.com/DojoManagement/dojo-tf-modules.git//dojo-apigw-deployment?ref=fix--create-one-api-gw-resource-by-path_part"
  
  redeploy_token = var.redeploy_token
}