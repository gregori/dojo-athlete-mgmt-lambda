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

module "lambda" {
  source = "git::https://github.com/DojoManagement/dojo-tf-modules.git//dojo-lambda?ref=dojo-lambda-0.0.2"

  lambda_name     = "dojo-athlete-mgmt" #####
  source_dir      = "../app"
  handler         = "lambda_function.lambda_handler"
  runtime_version = "python3.12"
  access_s3       = true
  env             = "stg"
  
  routes = [
    {
      method    = "POST"
      path_part = "register"
    },
    {
      method    = "POST"
      path_part = "update-profile"
    },
    {
      method    = "POST"
      path_part = "enroll"
    },
    {
      method    = "POST"
      path_part = "payment"
    },
    {
      method    = "POST"
      path_part = "checkin"
    }
  ]
}

module "lambda" {
  source = "git::https://github.com/DojoManagement/dojo-tf-modules.git//dojo-apigw-deployment?ref=dojo-apigw-deployment-0.0.1"
}