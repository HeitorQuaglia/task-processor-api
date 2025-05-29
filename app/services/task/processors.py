"""
Implementações de processadores para tarefas.
"""
import logging
from typing import Dict, Any, Optional, Union

from app.services.mongo_service import ITaskService
from app.services.task.interfaces import IUrlValidator, ICsvProcessor, IBackgroundTaskProcessor
from app.utils.csv_processor import process_csv
from app.utils.validator import validate_url

logger = logging.getLogger(__name__)


class DefaultUrlValidator(IUrlValidator):
    """Implementação padrão do validador de URLs."""
    def validate(self, url: str) -> Dict[str, Any]:
        """Valida uma URL usando o validador padrão."""
        return validate_url(url)


class DefaultCsvProcessor(ICsvProcessor):
    """Implementação padrão do processador de CSV."""
    def process(self, file_url: str, column_index: int) -> Dict[str, Any]:
        """Processa um arquivo CSV usando o processador padrão."""
        return process_csv(file_url, column_index)


class BackgroundTaskProcessor(IBackgroundTaskProcessor):
    """Processador de tarefas em background."""
    
    def __init__(self, 
                 task_service: ITaskService,
                 url_validator: IUrlValidator,
                 csv_processor: ICsvProcessor):
        """Inicializa o processador com os serviços necessários."""
        self.task_service = task_service
        self.url_validator = url_validator
        self.csv_processor = csv_processor
    
    async def update_task_status(self, task_id: str, status: str, 
                               result: Optional[Union[float, str]] = None, 
                               comment: str = "") -> None:
        """
        Atualiza o status da tarefa no MongoDB.
        :param task_id: ID único da tarefa
        :param status: Novo status da tarefa ('processing', 'completed', 'error')
        :param result: Resultado da tarefa (se aplicável)
        :param comment: Comentário ou mensagem sobre o status
        """
        try:
            await self.task_service.update_task(task_id, status, result, comment)
            logger.info(f"Task {task_id} atualizada: status={status}, result={result}, comment={comment}")
        except Exception as e:
            logger.error(f"Erro ao atualizar task {task_id}: {e}")
            raise
    
    async def validate_url(self, task_id: str, url: str) -> None:
        """
        Processa a URL (valida a URL) e atualiza o status no MongoDB.
        """
        try:
            result = self.url_validator.validate(url)
            await self.task_service.update_task(
                task_id, 
                result["status"], 
                result["result"], 
                result["comment"]
            )
            logger.info(f"URL {url} validada para task {task_id}")
        except Exception as e:
            logger.error(f"Erro ao validar URL {url} para task {task_id}: {e}")
            await self.task_service.update_task(
                task_id, 
                "error", 
                None, 
                f"Erro ao validar URL: {str(e)}"
            )
    
    async def process_csv(self, task_id: str, file_url: str, column_index: int) -> None:
        """
        Processa o CSV (valida a coluna) e atualiza o status no MongoDB.
        """
        try:
            result = self.csv_processor.process(file_url, column_index)
            await self.task_service.update_task(
                task_id, 
                result["status"], 
                result["result"], 
                result["comment"]
            )
            logger.info(f"CSV {file_url} processado para task {task_id}")
        except Exception as e:
            logger.error(f"Erro ao processar CSV {file_url} para task {task_id}: {e}")
            await self.task_service.update_task(
                task_id, 
                "error", 
                None, 
                f"Erro ao processar CSV: {str(e)}"
            )
