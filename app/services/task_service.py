from app.services.mongo_service import MongoService
import logging

from app.utils.csv_processor import process_csv
from app.utils.validator import validate_url

logger = logging.getLogger(__name__)

class TaskService:
    @staticmethod
    async def update_task_status(task_id: str, status: str, result=None, comment: str = ""):
        """
        Atualiza o status da tarefa no MongoDB.
        :param task_id: ID único da tarefa
        :param status: Novo status da tarefa ('processing', 'completed', 'error')
        :param result: Resultado da tarefa (se aplicável)
        :param comment: Comentário ou mensagem sobre o status
        """
        update_data = {"status": status, "result": result, "comment": comment}

        try:
            await MongoService.update_task(task_id, **update_data)
            logger.info(f"📌 Task {task_id} atualizada no MongoDB: {update_data}")
        except Exception as e:
            logger.error(f"❌ Erro ao atualizar task {task_id}: {e}")

    @staticmethod
    async def validate_url(task_id: str, url: str):
        """
        Processa a URL (valida a URL) e atualiza o status no MongoDB.
        """
        result = validate_url(url)

        result = {
            "status": "completed" if result["success"] else "error",
            "result": result["status"] if result["success"] else result["reason"],
            "comments": "A URL é válida" if result["success"] and result["status"] == "valid" else result["reason"]
        }

        await MongoService.update_task(task_id, result["status"] , result["result"], result["comment"])

    @staticmethod
    async def process_csv(task_id: str, file_url: str, column_name: str):
        """
        Processa o CSV (valida a coluna) e atualiza o status no MongoDB.
        """
        result = process_csv(file_url, column_name)

        await MongoService.update_task(task_id, result["status"], result["result"], result["comment"])