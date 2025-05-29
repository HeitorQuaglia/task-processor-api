import uuid
from fastapi import BackgroundTasks
from app.models.process_data_input import ProcessDataInput
from app.services.task_processor.processor import ProcessorProtocol
from app.services.task_processor.csv_processor import CSVProcessor
from app.services.task_processor.processor_response import ProcessorResponse
from app.services.task_processor.url_processor import UrlProcessor


class ProcessorService:
    @staticmethod
    async def process_data(background_tasks: BackgroundTasks, payload: ProcessDataInput) -> ProcessorResponse:
        """
        Processa os dados recebidos, cria a tarefa no MongoDB e delega a execução ao TaskService.
        """
        processor = ProcessorService.get_processor_for_payload(payload)
        return await processor.run(background_tasks)

    @staticmethod
    def get_processor_for_payload(payload: ProcessDataInput) -> ProcessorProtocol:
        if payload.file:
            return CSVProcessor(
                task_id=str(uuid.uuid4()),
                payload=payload.file,
                column=int(payload.column) if payload.column is not None else 0
            )
        if payload.url is None:
            raise ValueError("URL payload cannot be None")
        return UrlProcessor(
            task_id=str(uuid.uuid4()),
            payload=payload.url
        )