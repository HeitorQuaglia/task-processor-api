from fastapi import APIRouter

router = APIRouter()

@router.post("/process-data")
async def process_data(data: dict):
    return {"message": "Dados processados com sucesso"}