"""
Classes relacionadas ao upload de arquivos.
"""
import logging
from abc import abstractmethod
from http import HTTPStatus
from typing import Protocol

from fastapi import HTTPException, UploadFile
from botocore.exceptions import ClientError

from app.utils.error_messages import ErrorMessages
from app.utils.s3_utils import upload_to_s3

logger = logging.getLogger(__name__)


class IFileUploader(Protocol):
    """Interface para upload de arquivos."""
    @abstractmethod
    def upload(self, file: UploadFile) -> str:
        """Faz upload de um arquivo e retorna a URL."""
        pass


class S3FileUploader:
    """Implementação de upload de arquivos para S3."""
    def upload(self, file: UploadFile) -> str:
        """Faz upload de um arquivo para o S3 e retorna a URL."""
        try:
            file.file.seek(0)
            file_url = upload_to_s3(file)
            logger.info(f"Arquivo {file.filename} enviado para S3: {file_url}")
            return file_url
        except ClientError as e:
            logger.error(f"Erro de cliente S3 ao fazer upload do arquivo {file.filename}: {e}")
            raise HTTPException(status_code=HTTPStatus.SERVICE_UNAVAILABLE, 
                               detail=ErrorMessages.S3_UPLOAD_ERROR)
        except Exception as e:
            logger.error(f"Erro inesperado ao processar arquivo {file.filename}: {e}")
            raise HTTPException(status_code=HTTPStatus.INTERNAL_SERVER_ERROR, 
                               detail=ErrorMessages.UNEXPECTED_FILE_PROCESSING_ERROR)
