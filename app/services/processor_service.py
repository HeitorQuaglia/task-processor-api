import uuid
from http import HTTPStatus
from urllib.parse import urlparse

from botocore.exceptions import ClientError
from fastapi import BackgroundTasks, HTTPException

from app.models.process_data_input import ProcessDataInput
from app.models.task_result import TaskResult, UrlTaskData, CsvTaskData
from app.services.mongo_service import MongoService
from app.services.task_service import TaskService
from app.utils.error_messages import ErrorMessages
from app.utils.s3_utils import upload_to_s3


class ProcessorService:
    @staticmethod
    async def process_data(background_tasks: BackgroundTasks, payload: ProcessDataInput):
        """
        Processa os dados recebidos, cria a tarefa no MongoDB e delega a execução ao TaskService.
        """
        task_id = str(uuid.uuid4())

        response = {"task_id": task_id}

        if payload.file:
            try:
                if not payload.file.content_type.startswith("text") and not payload.file.filename.endswith(".csv"):
                    raise HTTPException(status_code=HTTPStatus.BAD_REQUEST, detail=ErrorMessages.INVALID_FILE_TYPE)

                payload.file.file.read()
                file_url = upload_to_s3(payload.file)
            except HTTPException:
                raise
            except ClientError as e:
                raise HTTPException(status_code=HTTPStatus.SERVICE_UNAVAILABLE, detail=ErrorMessages.S3_UPLOAD_ERROR)
            except Exception as e:
                raise HTTPException(status_code=HTTPStatus.INTERNAL_SERVER_ERROR, detail=ErrorMessages.UNEXPECTED_FILE_PROCESSING_ERROR)

            task_data = TaskResult(
                task_id=task_id,
                type="csv",
                status="processing",
                result=None,
                comment="Processando CSV...",
                task_metadata=CsvTaskData(file_url=file_url, column_name=payload.column)
            )

            response["file_url"] = file_url
            response["message"] = "Processando CSV..."
            await MongoService.save_task(task_data)
            background_tasks.add_task(TaskService.process_csv, task_id, file_url, int(payload.column))
        else:
            try:
                if not payload.url or not isinstance(payload.url, str):
                    raise HTTPException(status_code=HTTPStatus.BAD_REQUEST, detail=ErrorMessages.INVALID_URL)

                result = urlparse(payload.url)

                if not all([result.scheme, result.netloc]):
                    raise HTTPException(status_code=HTTPStatus.BAD_REQUEST, detail=ErrorMessages.INVALID_URL)

            except HTTPException:
                raise

            except Exception:
                raise HTTPException(status_code=HTTPStatus.INTERNAL_SERVER_ERROR, detail=ErrorMessages.URL_VALIDATION_ERROR)

            task_data = TaskResult(
                task_id=task_id,
                type="url",
                status="processing",
                result=None,
                comment="Validando URL...",
                task_metadata=UrlTaskData(url=payload.url)
            )

            response["url"] = payload.url
            response["message"] = "Processando validação de URL"
            await MongoService.save_task(task_data)
            background_tasks.add_task(TaskService.validate_url, task_id, payload.url)

        return response
