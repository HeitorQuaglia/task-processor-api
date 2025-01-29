import uuid
from app.models.task_result import TaskResult, UrlTaskData, CsvTaskData
from app.services.mongo_service import MongoService
from app.services.task_service import TaskService
from fastapi import BackgroundTasks, UploadFile, HTTPException
from app.models.process_data_input import ProcessDataInput
from app.utils.s3_utils import upload_to_s3


class ProcessorService:
    @staticmethod
    async def process_data(background_tasks: BackgroundTasks, payload: ProcessDataInput, file: UploadFile = None):
        """
        Processa os dados recebidos, cria a tarefa no MongoDB e delega a execução ao TaskService.
        """
        task_id = str(uuid.uuid4())

        response = {"task_id": task_id}

        if file:
            try:
                file_url = upload_to_s3(file)
            except Exception as e:
                raise HTTPException(status_code=503 , detail=str(e)) #TODO arrumar

            task_data = TaskResult(
                task_id=task_id,
                type="csv",
                status="processing",
                result=None,
                comment="Processando CSV...",
                task_data=CsvTaskData(file_url=file_url, column_name=payload.column)
            )

            response["file_url"] = file_url
            response["message"] = "Processando CSV..."
            await MongoService.save_task(task_data)
            background_tasks.add_task(TaskService.process_csv, task_id, file_url, payload.column)
        else:
            task_data = TaskResult(
                task_id=task_id,
                type="url",
                status="processing",
                result=None,
                comment="Validando URL...",
                task_data=UrlTaskData(url=payload.url)
            )

            response["url"] = payload.url
            response["message"] = "Processando validação de URL"
            await MongoService.save_task(task_data)
            background_tasks.add_task(TaskService.validate_url, task_id, payload.url)

        return response
