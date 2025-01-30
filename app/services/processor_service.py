import uuid
from urllib.parse import urlparse

from botocore.exceptions import ClientError

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
                if not file.content_type.startswith("text") and not file.filename.endswith(".csv"):
                    raise HTTPException(status_code=400, detail="Arquivo inválido. Apenas arquivos CSV são aceitos.")

                file.file.read()
                file_url = upload_to_s3(file)
            except ClientError as e:
                raise HTTPException(status_code=503, detail="Erro ao fazer upload do arquivo para S3.")
            except Exception as e:
                raise HTTPException(status_code=500, detail="Erro inesperado ao tentar processar o arquivo.")

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
                result = urlparse(payload.url)
                if not all([result.scheme, result.netloc]):
                    raise HTTPException(status_code=400, detail="URL fornecida é inválida.")
            except Exception:
                raise HTTPException(status_code=500, detail="Erro ao validar o formato da URL.")

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
