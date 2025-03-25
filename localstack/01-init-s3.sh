#!/bin/bash

# Espera o LocalStack iniciar completamente antes de fazer as requisições
echo "Esperando o LocalStack iniciar..."
sleep 5

# Cria um bucket S3
awslocal s3 mb s3://my-local-bucket
echo "Bucket S3 'my-local-bucket' criado."

awslocal s3 cp /etc/localstack/init/ready.d/athletes.csv s3://my-local-bucket/db/athletes.csv