from http import HTTPStatus
from typing import Optional
from fastapi import HTTPException, UploadFile, BackgroundTasks
from app.services.task_processor.processor import ProcessorProtocol
from app.services.task_processor.processor_response import CsvProcessorResponse
from app.services.task_service import TaskService
from app.utils.error_messages import ErrorMessages
from app.utils.s3_utils import upload_to_s3
from botocore.exceptions import ClientError
from app.models.task_result import TaskResult, CsvTaskData
from app.services.mongo_service import MongoService

class CSVProcessor(ProcessorProtocol):
    file_url: Optional[str]

    def __init__(self, task_id: str, payload: UploadFile, column: int):
        self.task_id = task_id
        self.payload = payload
        self.column = column  # keep as int for validation, convert to str only for CsvTaskData
        self.file_url: Optional[str] = None

    def validate(self) -> None:
        if not self.payload.content_type.startswith("text") and not self.payload.filename.endswith(".csv"):
            raise HTTPException(status_code=HTTPStatus.UNSUPPORTED_MEDIA_TYPE, detail=ErrorMessages.INVALID_FILE_TYPE)
        self.payload.file.seek(0)
        header = self.payload.file.readline().decode()
        if self.column < 0 or self.column >= len(header.split(',')):
            raise HTTPException(status_code=HTTPStatus.BAD_REQUEST, detail=ErrorMessages.INVALID_COLUMN_INDEX)
        self.payload.file.seek(0)

    def process(self) -> None:
        try:
            self.payload.file.seek(0)
            self.file_url = upload_to_s3(self.payload)
        except ClientError:
            raise HTTPException(status_code=HTTPStatus.SERVICE_UNAVAILABLE, detail=ErrorMessages.S3_UPLOAD_ERROR)
        except Exception:
            raise HTTPException(status_code=HTTPStatus.INTERNAL_SERVER_ERROR, detail=ErrorMessages.UNEXPECTED_FILE_PROCESSING_ERROR)

    def create_task_data(self) -> TaskResult:
        if not self.file_url:
            raise HTTPException(status_code=HTTPStatus.INTERNAL_SERVER_ERROR, detail=ErrorMessages.FILE_NOT_UPLOADED)
        return TaskResult(
            task_id=self.task_id,
            type="csv",
            status="processing",
            result=None,
            comment="Processando CSV...",
            task_metadata=CsvTaskData(file_url=self.file_url, column_name=str(self.column))
        )

    async def save_task(self, task_data: TaskResult):
        await MongoService.save_task(task_data)

    def add_background_task(self, background_tasks: BackgroundTasks) -> None:
        if not self.file_url:
            raise HTTPException(status_code=HTTPStatus.INTERNAL_SERVER_ERROR, detail=ErrorMessages.FILE_NOT_UPLOADED)
        background_tasks.add_task(TaskService.process_csv, self.task_id, self.file_url, self.column)

    def response(self) -> CsvProcessorResponse:
        if not self.file_url:
            raise HTTPException(status_code=HTTPStatus.INTERNAL_SERVER_ERROR, detail=ErrorMessages.FILE_NOT_UPLOADED)
        return CsvProcessorResponse(
            task_id=self.task_id,
            file_url=self.file_url,
            message="Processando CSV..."
        )