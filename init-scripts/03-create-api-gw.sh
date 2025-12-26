#!/bin/bash
# filepath: /d/dojo-athlete-mgmt-lambda/init-scripts/register-apigw-athletes.sh

set -e

# 1. Cria a API REST
API_ID=$(awslocal apigateway create-rest-api --name athlete-api --query 'id' --output text)

# 2. Obtém o ID do recurso raiz
ROOT_ID=$(awslocal apigateway get-resources --rest-api-id $API_ID --query 'items[?path==`/`].id' --output text)

# 3. Cria o recurso /athletes
ATHLETES=$(awslocal apigateway create-resource --rest-api-id $API_ID --parent-id $ROOT_ID --path-part athletes --query 'id' --output text)

# 4. Adiciona métodos GET e POST
awslocal apigateway put-method --rest-api-id $API_ID --resource-id $ATHLETES --http-method GET --authorization-type "NONE"
awslocal apigateway put-method --rest-api-id $API_ID --resource-id $ATHLETES --http-method POST --authorization-type "NONE"

# 5. Integra os métodos à Lambda
LAMBDA_ARN="arn:aws:lambda:us-east-1:000000000000:function:dojo-athlete-mgmt-lambda"
APIGW_URI="arn:aws:apigateway:us-east-1:lambda:path/2015-03-31/functions/$LAMBDA_ARN/invocations"

for METHOD in GET POST; do
  awslocal apigateway put-integration \
    --rest-api-id $API_ID \
    --resource-id $ATHLETES \
    --http-method $METHOD \
    --type AWS_PROXY \
    --integration-http-method POST \
    --uri $APIGW_URI
done

# 6. Dá permissão à Lambda para ser chamada pelo API Gateway
awslocal lambda add-permission \
  --function-name dojo-athlete-mgmt-lambda \
  --statement-id apigateway-athletes \
  --action lambda:InvokeFunction \
  --principal apigateway.amazonaws.com \
  --source-arn "arn:aws:execute-api:us-east-1:000000000000:$API_ID/*/*/athletes" 2>/dev/null || echo "Permissão já existe"

## 7. Implanta a API
#awslocal apigateway create-deployment --rest-api-id $API_ID --stage-name dev

# 8. Cria o recurso /athletes/{id}
ATHLETES_ID=$(awslocal apigateway create-resource --rest-api-id $API_ID --parent-id $ATHLETES --path-part "{id}" --query 'id' --output text)

# 9. Adiciona método GET para /athletes/{id}
for METHOD_ID in GET PUT DELETE; do
  awslocal apigateway put-method --rest-api-id $API_ID --resource-id $ATHLETES_ID --http-method $METHOD_ID --authorization-type "NONE"
done

# 10. Integra o método GET e DELETE à Lambda
for METHOD_ID in GET DELETE PUT; do
  awslocal apigateway put-integration \
    --rest-api-id $API_ID \
    --resource-id $ATHLETES_ID \
    --http-method $METHOD_ID \
    --type AWS_PROXY \
    --integration-http-method POST \
    --uri $APIGW_URI
done

# 11. Dá permissão à Lambda para ser chamada pelo API Gateway para o novo recurso
for METHOD_ID in GET DELETE PUT; do
  awslocal lambda add-permission \
    --function-name dojo-athlete-mgmt-lambda \
    --statement-id "apigateway-athletes-$METHOD_ID" \
    --action lambda:InvokeFunction \
    --principal apigateway.amazonaws.com \
    --source-arn "arn:aws:execute-api:us-east-1:000000000000:$API_ID/*/$METHOD_ID/athletes/*" 2>/dev/null || echo "Permissão $METHOD_ID já existe"
done

# 12. Implanta a API
awslocal apigateway create-deployment --rest-api-id $API_ID --stage-name dev



echo "==================================="
echo "API Gateway criado com sucesso!"
echo "==================================="
echo "Rotas disponíveis:"
echo "GET    /athletes       - Listar todos"
echo "POST   /athletes       - Criar novo"
echo "GET    /athletes/{id}  - Buscar por ID"
echo "PUT    /athletes/{id}  - Atualizar"
echo "DELETE /athletes/{id}  - Deletar"
echo "==================================="
echo "Endpoint base:"
echo "http://localhost:4566/restapis/$API_ID/dev/_user_request_/athletes"
echo "$API_ID"
echo "==================================="