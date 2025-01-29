from fastapi import APIRouter, UploadFile, File, Depends, BackgroundTasks, HTTPException, Request

from app.services.mongo_service import MongoService
from app.services.processor_service import ProcessorService
from app.models.process_data_input import ProcessDataInput

router = APIRouter()

@router.post("/process-data")
async def process_data(background_tasks: BackgroundTasks, payload: ProcessDataInput):
    file = None
    return await ProcessorService.process_data(background_tasks, payload, file)

@router.get("/results/{task_id}")
async def get_task_result(task_id: str):
    """
    Consulta o status de uma tarefa pelo ID.
    """
    # Recupera a task pelo ID
    task = await MongoService.get_task(task_id)

    if not task:
        raise HTTPException(status_code=404, detail="Task não encontrada")

    # Retorna os dados da task
    return {"task_id": task.task_id, "status": task.status, "result": task.result, "comment": task.comment}