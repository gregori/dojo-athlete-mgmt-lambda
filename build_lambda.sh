#!/bin/bash

set -e  # Encerra o script se algum comando falhar

# Diretórios e arquivos
SOURCE_DIR="app"                        # Altere se o código estiver em outro lugar
BUILD_DIR="lambda_build"
ZIP_FILE="lambda_package.zip"
REQUIREMENTS_FILE="$SOURCE_DIR/requirements.txt"

echo "🔧 Limpando build anterior..."
rm -rf "$BUILD_DIR" "$ZIP_FILE"

echo "📁 Criando diretório de build: $BUILD_DIR"
mkdir -p "$BUILD_DIR"

echo "📦 Instalando dependências do requirements.txt..."
pip install -r "$REQUIREMENTS_FILE" -t "$BUILD_DIR"

echo "📄 Copiando arquivos da aplicação para o diretório de build..."
cp -r "$SOURCE_DIR"/* "$BUILD_DIR/"

echo "✅ Build completo: $BUILD_DIR está pronto para uso no Terraform"

# Copie outros diretórios necessários (modifique conforme seu projeto)
#if [ -d "$SOURCE_DIR/athletemgmt" ]; then
#  cp -r "$SOURCE_DIR/dojocommons" "$BUILD_DIR/"
#fi

#echo "🗜️ Criando o pacote .zip: $ZIP_FILE"
#cd "$BUILD_DIR"
#zip -r "../$ZIP_FILE" .
#cd ..

#echo "✅ Build completo: $ZIP_FILE está pronto para uso no Terraform"
