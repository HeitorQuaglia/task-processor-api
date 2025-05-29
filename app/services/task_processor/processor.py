from abc import ABC
from typing import Any

from fastapi import BackgroundTasks

from app.models.task_result import TaskResult
from app.services.task_processor.interfaces import IProcessorProtocol
from app.services.task_processor.processor_response import ProcessorResponse


class ProcessorProtocol(ABC, IProcessorProtocol):
    """Implementação base do protocolo para processadores de tarefas."""
    task_id: str
    payload: Any

    async def run(self, background_tasks: BackgroundTasks) -> ProcessorResponse:
        """
        Executa o pipeline padrão de processamento:
        1. Valida entrada
        2. Processa dados
        3. Cria estrutura da task
        4. Salva no banco
        5. Adiciona tarefa em background
        6. Retorna resposta
        """
        # Template Method Pattern - define o esqueleto do algoritmo
        self.validate()
        self.process()
        task_data = self.create_task_data()
        await self.save_task(task_data)
        self.add_background_task(background_tasks)
        return self.response()
