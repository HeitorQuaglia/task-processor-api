"""
Implementação do serviço de MongoDB.
"""
import logging
from typing import Optional, Union

from app.models.task_result import TaskResult
from app.repositories.interfaces import ITaskRepository
from app.services.mongo.interfaces import ITaskService, TaskStatus

logger = logging.getLogger(__name__)


class TaskService(ITaskService):
    """Implementação do serviço de tarefas usando um repositório."""
    
    def __init__(self, repository: ITaskRepository):
        """Inicializa o serviço com um repositório de tarefas."""
        self.repository = repository

    async def save_task(self, task: TaskResult) -> None:
        """Salva uma nova tarefa no repositório."""
        await self.repository.save_task(task)
        logger.info(f"Task {task.task_id} saved via service")

    async def get_task(self, task_id: str) -> TaskResult:
        """Recupera uma tarefa pelo ID do repositório."""
        task = await self.repository.get_task(task_id)
        if not task:
            error_msg = f"Tarefa com task_id {task_id} não encontrada."
            logger.error(error_msg)
            raise ValueError(error_msg)
        return task

    async def update_task(self, task_id: str, status: TaskStatus, 
                         result: Optional[Union[float, str]] = None, 
                         comment: str = "") -> None:
        """Atualiza o status de uma tarefa existente."""
        try:
            task = await self._get_task_or_raise(task_id)
            task_dict = task.dict()
            task_dict.update({
                "status": status,
                "result": result,
                "comment": comment
            })
            task_updated = TaskResult(**task_dict)
            await self.repository.update_task(task_updated)
            logger.info(f"Task {task_id} updated with status {status}")
        except Exception as e:
            logger.error(f"Error updating task {task_id}: {e}")
            raise

    async def _get_task_or_raise(self, task_id: str) -> TaskResult:
        """Recupera uma tarefa ou lança uma exceção se não encontrada."""
        task = await self.repository.get_task(task_id)
        if not task:
            error_msg = f"Tarefa com task_id {task_id} não encontrada."
            logger.error(error_msg)
            raise ValueError(error_msg)
        return task
