#from athletemgmt.model.event import Event
#
#
#def lambda_handler(event, _):
#    event_obj = Event.model_validate(event)
#
#    return {
#        "statusCode": 200,
#        "body": event_obj.model_dump()
#    }

import json
import boto3
import uuid
import datetime

# Configuração do S3
S3_BUCKET = "dojo-athlete-mgmt-lambda"
s3_client = boto3.client("s3")

# Caminhos dos arquivos no S3
AULAS_FILE = "aulas.json"
PRESENCAS_FILE = "presencas.json"

def carregar_dados(arquivo):
    """Carrega os dados de um arquivo no S3."""
    try:
        response = s3_client.get_object(Bucket=S3_BUCKET, Key=arquivo)
        return json.loads(response["Body"].read().decode("utf-8"))
    except s3_client.exceptions.NoSuchKey:
        return []  # Retorna lista vazia

def salvar_dados(arquivo, dados):
    """Salva os dados no S3."""
    s3_client.put_object(Bucket=S3_BUCKET, Key=arquivo, Body=json.dumps(dados))

def cadastrar_aula(event, context):
    """Função Lambda para cadastrar uma nova aula."""
    body = json.loads(event["body"])
    nome = body.get("nome")
    horario = body.get("horario")
    dia_semana  = body.get("dia_semana")
    dojo  = body.get("dojo")
    
    if not nome or not horario or not dia_semana or not dojo:
        return {"statusCode": 400, "body": json.dumps({"error": "Nome, horário, dia da semana e Dojo são obrigatórios"})}
    
    aulas = carregar_dados(AULAS_FILE)
    nova_aula = {"id": str(uuid.uuid4()), "nome": nome, "horario": horario, "dia_semana": dia_semana, "dojo": dojo}
    aulas.append(nova_aula)
    salvar_dados(AULAS_FILE, aulas)
    
    return {"statusCode": 200, "body": json.dumps(nova_aula)}

def fazer_checkin(event, context):
    """Função Lambda para registrar presença de um aluno."""
    body = json.loads(event["body"])
    nome = body.get("nome")
    codigo = body.get("codigo")
    aula_id = body.get("aula_id")
    
    if not nome or not codigo or not aula_id:
        return {"statusCode": 400, "body": json.dumps({"error": "Todos os campos são obrigatórios"})}
    
    presencas = carregar_dados(PRESENCAS_FILE)
    nova_presenca = {
        "id": str(uuid.uuid4()),
        "nome": nome,
        "codigo": codigo,
        "aula_id": aula_id,
        "data": str(datetime.datetime.utcnow())
    }
    presencas.append(nova_presenca)
    salvar_dados(PRESENCAS_FILE, presencas)
    
    return {"statusCode": 200, "body": json.dumps(nova_presenca)}

def listar_presencas(query_params, context):
    """Função Lambda para listar presenças de uma aula específica."""
    if not query_params:
        return {"statusCode": 400, "body": json.dumps({"error": "Parâmetros não fornecidos"})}
    
    aula_id = query_params.get("aula_id")
    if not aula_id:
        return {"statusCode": 400, "body": json.dumps({"error": "Aula ID é obrigatório"})}
    
    presencas = carregar_dados(PRESENCAS_FILE)
    presencas_filtradas = [p for p in presencas if p["aula_id"] == aula_id]
    
    return {"statusCode": 200, "body": json.dumps(presencas_filtradas)}

def lambda_handler(event, context):
    """Função principal da Lambda, roteia chamadas para as funções corretas."""
    http_method = event.get("httpMethod")
    path = event.get("path")
    body = json.loads(event.get("body", "{}")) if http_method in ["POST", "PUT"] else {}
    query_params = event.get("queryStringParameters", {})

    if path == "/aulas" and http_method == "POST":
        return cadastrar_aula(event, context)
    elif path == "/checkin" and http_method == "POST":
        return fazer_checkin(event, context)
    elif path == "/presencas" and http_method == "GET":
        return listar_presencas(query_params, context)
    else:
        return {"statusCode": 404, "body": json.dumps({"error": "Rota não encontrada"})}

