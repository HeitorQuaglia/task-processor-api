from app.models.process_data_input import ProcessDataInput
from app.services.celery_service import CeleryService
from app.utils.file_utils import upload_to_s3

from fastapi import UploadFile

class ProcessorService:
    @staticmethod
    async def process_data(payload: ProcessDataInput, file: UploadFile = None):
        """
        Processa os dados recebidos e direciona para a fila correta (URL ou CSV).
        """
        if file:
            file_url = upload_to_s3(file)
            return CeleryService.enqueue_csv_task(file_url, payload.column_name)

        return CeleryService.enqueue_url_task(payload.url)
