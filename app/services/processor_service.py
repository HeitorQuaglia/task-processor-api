from fastapi import BackgroundTasks, UploadFile
from app.models.process_data_input import ProcessDataInput
from app.services.task_service import TaskService
from app.services.mongo_service import MongoService
from app.models.task_result import TaskResult
from app.utils.s3_utils import upload_to_s3
import uuid

class ProcessorService:
    @staticmethod
    async def process_data(background_tasks: BackgroundTasks, payload: ProcessDataInput, file: UploadFile = None):
        """
        Processa os dados recebidos, cria a tarefa no MongoDB e delega a execução ao TaskService.
        """
        task_id = str(uuid.uuid4())

        task_data = TaskResult(
            task_id=task_id,
            type="file" if file else "url",
            status="processing",
            result=None,
            comment="Processando dados..."
        )
        await MongoService.save_task(task_data)

        if file:
            file_url = upload_to_s3(file)
            background_tasks.add_task(TaskService.process_csv, file_url, payload.column_name, task_id)
            return {"message": "Processamento de CSV iniciado.", "task_id": task_id, "file_url": file_url}

        background_tasks.add_task(TaskService.validate_url, payload.url, task_id)
        return {"message": "Validação de URL iniciada.", "task_id": task_id, "url": payload.url}