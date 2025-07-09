#!/bin/bash
set -e

# Caminho temporário para empacotar a lambda
TMP_DIR=/tmp/lambda_package

# Limpa e cria o diretório temporário
rm -rf $TMP_DIR
mkdir -p $TMP_DIR

# Copia o código da lambda
cp -r /tmp/code/* $TMP_DIR/

# Instala as dependências (se existir requirements.txt)
if [ -f /tmp/code/requirements.txt ]; then
  pip install -r /tmp/code/requirements.txt --target $TMP_DIR
fi

# Empacota tudo em um zip
cd $TMP_DIR
zip -r /tmp/lambda_function.zip .

# Cria a função Lambda no LocalStack
awslocal lambda create-function \
  --function-name dojo-athlete-mgmt-lambda \
  --runtime python3.11 \
  --handler lambda_function.lambda_handler \
  --role arn:aws:iam::000000000000:role/lambda-role \
  --zip-file fileb:///tmp/lambda_function.zip \
  --timeout 30
