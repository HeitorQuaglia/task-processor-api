import logging
from http import HTTPStatus
from typing import Any
from urllib.parse import urlparse

from fastapi import HTTPException, BackgroundTasks

from app.models.task_result import TaskResult, UrlTaskData
from app.services.mongo_service import default_mongo_service, ITaskService
from app.services.task_processor.processor import ProcessorProtocol
from app.services.task_processor.processor_response import UrlProcessorResponse
from app.services.task_service import TaskService
from app.utils.error_messages import ErrorMessages

logger = logging.getLogger(__name__)


class IUrlValidator:
    """Interface para validação de URLs."""
    def validate(self, url: str) -> bool:
        """Valida uma URL e retorna True se for válida."""
        pass


class UrlParseValidator(IUrlValidator):
    """Validador de URL usando urlparse."""
    def validate(self, url: str) -> bool:
        """Valida uma URL usando urlparse."""
        if not url or not isinstance(url, str):
            return False
        
        result = urlparse(url)
        return all([result.scheme, result.netloc])


class UrlProcessor(ProcessorProtocol):
    """Processador de URLs."""
    
    def __init__(self, task_id: str, payload: str, 
                 url_validator: IUrlValidator = None,
                 task_service: ITaskService = None):
        """Inicializa o processador com os dados necessários."""
        self.task_id = task_id
        self.payload = payload
        self.url_validator = url_validator or UrlParseValidator()
        self.task_service = task_service or default_mongo_service

    def validate(self) -> None:
        """Valida a URL fornecida."""
        if not self.url_validator.validate(self.payload):
            logger.warning(f"URL inválida: {self.payload}")
            raise HTTPException(status_code=HTTPStatus.BAD_REQUEST, 
                               detail=ErrorMessages.INVALID_URL)
        logger.info(f"URL válida: {self.payload}")

    def process(self) -> None:
        """Processa a URL (neste caso, não há processamento adicional)."""
        # Não há processamento adicional para URLs após a validação
        logger.info(f"URL processada: {self.payload}")
        pass

    def create_task_data(self) -> TaskResult:
        """Cria os dados da tarefa para validação de URL."""
        return TaskResult(
            task_id=self.task_id,
            type="url",
            status="processing",
            result=None,
            comment="Validando URL...",
            task_metadata=UrlTaskData(url=self.payload)
        )

    async def save_task(self, task_data: TaskResult) -> None:
        """Salva a tarefa no repositório."""
        await self.task_service.save_task(task_data)
        logger.info(f"Tarefa URL salva: {task_data.task_id}")

    def add_background_task(self, background_tasks: BackgroundTasks) -> None:
        """Adiciona a tarefa de validação em background."""
        background_tasks.add_task(TaskService.validate_url, self.task_id, self.payload)
        logger.info(f"Tarefa em background adicionada para validar URL: {self.task_id}, {self.payload}")

    def response(self) -> UrlProcessorResponse:
        """Cria a resposta do processador."""
        return UrlProcessorResponse(
            task_id=self.task_id,
            url=self.payload,
            message="Processando validação de URL"
        )