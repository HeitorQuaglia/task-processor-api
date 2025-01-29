from pydantic import BaseModel, Field
from typing import Optional, Literal


class TaskResult(BaseModel):
    task_id: str = Field(..., description="ID único da tarefa Celery")
    type: Literal["url", "file"] = Field(..., description="Tipo da tarefa: URL ou arquivo CSV")
    status: Literal["processing", "error", "completed"] = Field(..., description="Status da tarefa")
    result: Optional[float] = Field(None, description="Resultado numérico ou booleano da operação")
    comment: Optional[str] = Field(None, description="Comentário sobre o resultado")
