from typing import Optional
from fastapi import APIRouter, BackgroundTasks, HTTPException, File, Form, UploadFile

from app.models.process_data_input import ProcessDataInput
from app.services.mongo_service import MongoService
from app.services.processor_service import ProcessorService

router = APIRouter()

@router.post("/process-data")
async def process_data(
    background_tasks: BackgroundTasks,
    url: Optional[str] = Form(None),
    column: Optional[str] = Form(None),
    file: UploadFile = File(None),
):
    try:
        payload = ProcessDataInput(url=url, column=column, file=file)
    except ValueError as e:
        error_message = e.errors()[0]["msg"]
        raise HTTPException(status_code=400, detail=error_message)
    return await ProcessorService.process_data(background_tasks, payload, file)

@router.get("/results/{task_id}")
async def get_task_result(task_id: str):
    """
    Consulta o status de uma tarefa pelo ID.
    """
    task = await MongoService.get_task(task_id)

    if not task:
        raise HTTPException(status_code=404, detail="Task não encontrada")

    return task