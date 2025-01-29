from fastapi import APIRouter, UploadFile, File, Depends

from app.models.schemas import ProcessDataInput

router = APIRouter()

@router.post("/process-data")
async def process_data(payload: ProcessDataInput = Depends(), file: UploadFile = File(None)):
    return {"message": "Dados recebidos!", "data": payload.dict(), "file": file.filename if file else None}