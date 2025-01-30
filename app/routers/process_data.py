from http import HTTPStatus
from typing import Optional
from fastapi import APIRouter, BackgroundTasks, HTTPException, File, Form, UploadFile
from app.models.process_data_input import ProcessDataInput
from app.services.mongo_service import MongoService
from app.services.processor_service import ProcessorService
from app.utils.error_messages import ErrorMessages

router = APIRouter()

def format_payload(url: Optional[str], column: Optional[str], file: UploadFile) -> ProcessDataInput:
    """Função auxiliar para criar e validar o payload."""
    try:
        return ProcessDataInput(url=url, column=column, file=file)
    except ValueError as e:
        error_message = e.errors()[0]["msg"]
        raise HTTPException(status_code=HTTPStatus.BAD_REQUEST, detail=error_message)


async def fetch_task_or_404(task_id: str):
    """Verifica se a tarefa existe, caso contrário, lança erro 404."""
    task = await MongoService.get_task(task_id)
    if not task:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail=ErrorMessages.TASK_NOT_FOUND_MSG)
    return task


@router.post("/process-data")
async def process_data(
        background_tasks: BackgroundTasks,
        url: Optional[str] = Form(None),
        column: Optional[str] = Form(None),
        file: UploadFile = File(None),
):
    payload = format_payload(url, column, file)
    return await ProcessorService.process_data(background_tasks, payload)


@router.get("/results/{task_id}")
async def fetch_task_status(task_id: str):
    """Consulta o status de uma tarefa pelo ID."""
    task = await fetch_task_or_404(task_id)
    return task