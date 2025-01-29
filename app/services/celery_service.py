from app.tasks.worker import validate_link, process_csv
from app.services.mongo_service import MongoService
from app.models.task_result import TaskResult

class CeleryService:
    @staticmethod
    def enqueue_url_task(url: str):
        task = validate_link.delay(url)

        # Salva no MongoDB
        MongoService.save_task(TaskResult(
            task_id=task.id,
            type="url",
            status="processing",
            result=None,
            comment="Validação em andamento."
        ))

        return {"message": "Validação de URL iniciada.", "task_id": task.id}

    @staticmethod
    def enqueue_csv_task(file_url: str, column_name: str):
        task = process_csv.delay(file_url, column_name)

        # Salva no MongoDB
        MongoService.save_task(TaskResult(
            task_id=task.id,
            type="file",
            status="processing",
            result=None,
            comment=f"Processando coluna '{column_name}'."
        ))

        return {"message": "Processamento de CSV iniciado.", "task_id": task.id}
