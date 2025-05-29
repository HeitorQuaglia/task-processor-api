import logging
from http import HTTPStatus
from typing import Optional

from fastapi import HTTPException, UploadFile, BackgroundTasks

from app.models.task_result import TaskResult, CsvTaskData
from app.services.file.file_uploader import IFileUploader, S3FileUploader
from app.services.mongo_service import default_mongo_service, ITaskService
from app.services.task_processor.processor import ProcessorProtocol
from app.services.task_processor.processor_response import CsvProcessorResponse
from app.services.task_service import TaskService
from app.utils.error_messages import ErrorMessages

logger = logging.getLogger(__name__)


class CSVProcessor(ProcessorProtocol):
    """Processador de arquivos CSV."""
    
    def __init__(self, task_id: str, payload: UploadFile, column: int, 
                 file_uploader: IFileUploader = None,
                 task_service: ITaskService = None):
        """Inicializa o processador com os dados necessários."""
        self.task_id = task_id
        self.payload = payload
        self.column = column  # keep as int for validation, convert to str only for CsvTaskData
        self.file_url: Optional[str] = None
        # Injeção de dependências
        self.file_uploader = file_uploader or S3FileUploader()
        self.task_service = task_service or default_mongo_service

    def validate(self) -> None:
        """Valida o arquivo CSV e a coluna especificada."""
        # Validação do tipo de arquivo
        if not self.payload.content_type.startswith("text") and not self.payload.filename.endswith(".csv"):
            logger.warning(f"Tipo de arquivo inválido: {self.payload.content_type}, {self.payload.filename}")
            raise HTTPException(status_code=HTTPStatus.UNSUPPORTED_MEDIA_TYPE, 
                               detail=ErrorMessages.INVALID_FILE_TYPE)
        
        # Validação da coluna
        try:
            self.payload.file.seek(0)
            header = self.payload.file.readline().decode()
            if self.column < 0 or self.column >= len(header.split(',')):
                logger.warning(f"Índice de coluna inválido: {self.column}")
                raise HTTPException(status_code=HTTPStatus.BAD_REQUEST, 
                                  detail=ErrorMessages.INVALID_COLUMN_INDEX)
            self.payload.file.seek(0)
            logger.info(f"Arquivo CSV validado com sucesso: {self.payload.filename}, coluna: {self.column}")
        except UnicodeDecodeError as e:
            logger.error(f"Erro ao decodificar o arquivo CSV: {e}")
            raise HTTPException(status_code=HTTPStatus.BAD_REQUEST, 
                               detail=ErrorMessages.INVALID_FILE_FORMAT)

    def process(self) -> None:
        """Processa o arquivo CSV (faz upload para S3)."""
        self.file_url = self.file_uploader.upload(self.payload)
        logger.info(f"Arquivo processado e enviado para S3: {self.file_url}")

    def create_task_data(self) -> TaskResult:
        """Cria os dados da tarefa para processamento de CSV."""
        if not self.file_url:
            logger.error("Tentativa de criar task_data sem URL de arquivo")
            raise HTTPException(status_code=HTTPStatus.INTERNAL_SERVER_ERROR, 
                               detail=ErrorMessages.FILE_NOT_UPLOADED)
        
        return TaskResult(
            task_id=self.task_id,
            type="csv",
            status="processing",
            result=None,
            comment="Processando CSV...",
            task_metadata=CsvTaskData(file_url=self.file_url, column_name=str(self.column))
        )

    async def save_task(self, task_data: TaskResult) -> None:
        """Salva a tarefa no repositório."""
        await self.task_service.save_task(task_data)
        logger.info(f"Tarefa CSV salva: {task_data.task_id}")

    def add_background_task(self, background_tasks: BackgroundTasks) -> None:
        """Adiciona a tarefa de processamento em background."""
        if not self.file_url:
            logger.error("Tentativa de adicionar tarefa em background sem URL de arquivo")
            raise HTTPException(status_code=HTTPStatus.INTERNAL_SERVER_ERROR, 
                               detail=ErrorMessages.FILE_NOT_UPLOADED)
        
        background_tasks.add_task(TaskService.process_csv, self.task_id, self.file_url, self.column)
        logger.info(f"Tarefa em background adicionada para processar CSV: {self.task_id}, {self.file_url}")

    def response(self) -> CsvProcessorResponse:
        """Cria a resposta do processador."""
        if not self.file_url:
            logger.error("Tentativa de criar resposta sem URL de arquivo")
            raise HTTPException(status_code=HTTPStatus.INTERNAL_SERVER_ERROR, 
                               detail=ErrorMessages.FILE_NOT_UPLOADED)
        
        return CsvProcessorResponse(
            task_id=self.task_id,
            file_url=self.file_url,
            message="Processando CSV..."
        )