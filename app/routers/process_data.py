from fastapi import APIRouter, UploadFile, File, Depends

from app.services.processor_service import ProcessorService
from app.models.process_data_input import ProcessDataInput

router = APIRouter()

@router.post("/process-data")
async def process_data(payload: ProcessDataInput = Depends(ProcessDataInput), file: UploadFile = File(None)):
    return await ProcessorService.process_data(payload, file)