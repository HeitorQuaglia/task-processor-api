from http import HTTPStatus
from typing import Any
from urllib.parse import urlparse

from fastapi import HTTPException, BackgroundTasks

from app.models.task_result import TaskResult, UrlTaskData
from app.services.mongo_service import MongoService
from app.services.task_processor.processor import ProcessorProtocol
from app.services.task_processor.processor_response import UrlProcessorResponse
from app.services.task_service import TaskService
from app.utils.error_messages import ErrorMessages


class UrlProcessor(ProcessorProtocol):
    def __init__(self, task_id: str, payload: str):
        self.task_id = task_id
        self.payload = payload

    def validate(self) -> None:
        if not self.payload or not isinstance(self.payload, str):
            raise HTTPException(status_code=HTTPStatus.BAD_REQUEST, detail=ErrorMessages.INVALID_URL)

    def process(self) -> None:
        result = urlparse(self.payload)
        if not all([result.scheme, result.netloc]):
            raise HTTPException(status_code=HTTPStatus.BAD_REQUEST, detail=ErrorMessages.INVALID_URL)

    def create_task_data(self) -> TaskResult:
        return TaskResult(
            task_id=self.task_id,
            type="url",
            status="processing",
            result=None,
            comment="Validando URL...",
            task_metadata=UrlTaskData(url=self.payload)
        )

    async def save_task(self, task_data: TaskResult):
        await MongoService.save_task(task_data)

    def add_background_task(self, background_tasks: BackgroundTasks) -> None:
        background_tasks.add_task(TaskService.validate_url, self.task_id, self.payload)

    def response(self) -> UrlProcessorResponse:
        return UrlProcessorResponse(
            task_id=self.task_id,
            url=self.payload,
            message="Processando validação de URL"
        )