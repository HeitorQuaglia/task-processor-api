import logging
from http import HTTPStatus

import boto3
import os
from fastapi import UploadFile, HTTPException
from uuid import uuid4

from app.utils.error_messages import ErrorMessages

logger = logging.getLogger(__name__)

# Configurações do S3
AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
AWS_BUCKET_NAME = os.getenv("AWS_BUCKET_NAME")
AWS_REGION = os.getenv("AWS_REGION")
AWS_URL = os.getenv("AWS_URL")

# Criar cliente do S3
s3_client = boto3.client(
    "s3",
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
    region_name=AWS_REGION,
    endpoint_url=AWS_URL
)


def upload_to_s3(file: UploadFile) -> str:
    """
    Faz o upload de um arquivo para o S3 e retorna a URL pública do arquivo.
    """
    try:
        file_extension = file.filename.split(".")[-1]
        file_key = f"uploads/{uuid4()}.{file_extension}"

        s3_client.upload_fileobj(file.file, AWS_BUCKET_NAME, file_key, ExtraArgs={"ACL": "public-read"})

        file_url = f"https://{AWS_BUCKET_NAME}.s3.{AWS_REGION}.amazonaws.com/{file_key}"
        return file_url
    except Exception as e:
        logger.error(f"Erro ao fazer upload para o S3: {e}")
        raise


def download_from_s3(file_key: str):
    """
    Faz o download de um arquivo do S3 e retorna o conteúdo do arquivo.
    :param file_key: A chave do arquivo no S3.
    :return: O conteúdo do arquivo.
    """
    try:
        file_obj = s3_client.get_object(Bucket=AWS_BUCKET_NAME, Key=f"uploads/{file_key}")
        return file_obj['Body'].read()
    except Exception as e:
        logger.error(f"Erro ao fazer download do arquivo {file_key} do S3: {e}")
        raise HTTPException(status_code=HTTPStatus.INTERNAL_SERVER_ERROR, detail=ErrorMessages.FILE_DOWNLOAD_ERROR)
