import requests
import logging
from app.config.celery_config import celery

logger = logging.getLogger(__name__)

@celery.task
def validate_link(url: str):
    """
    Valida se uma URL é acessível retornando o status.
    """
    try:
        response = requests.head(url, allow_redirects=True, timeout=(3, 5))  # (connect_timeout, read_timeout)
        if response.status_code == 200:
            return {"url": url, "status": "valid"}
        return {"url": url, "status": "invalid", "reason": f"Status code {response.status_code}"}
    except requests.RequestException as e:
        logger.error(f"Erro ao validar URL {url}: {e}")
        return {"url": url, "status": "invalid", "reason": str(e)}

@celery.task
def process_csv(file_url: str, column_name: str):
    """
    TODO: Implementar a validação do CSV armazenado no S3.
    Deve:
    - Baixar o arquivo do S3 via URL
    - Verificar se a coluna `column_name` existe
    - Retornar erro se a coluna não existir
    - Retornar sucesso com os metadados do arquivo se for válido
    """
    pass
