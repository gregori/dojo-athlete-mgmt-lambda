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

variable "env" {
  default = ""
  type    = string
}

module "lambda" {
  source = "git::https://github.com/DojoManagement/dojo-tf-modules.git//dojo-lambda?ref=dojo-lambda-0.0.1"

  lambda_name     = "dojo-athlete-mgmt" #####
  source_file     = "../app/lambda_function" #without extension
  handler         = "lambda_function.lambda_handler"
  runtime_version = "python3.12"
  access_s3       = bool
  env             = var.env
  
  routes = [
    {
      method    = "GET"
      path_part = "path1"
    },
    {
      method    = "POST"
      path_part = "path2"
    }
  ]
}