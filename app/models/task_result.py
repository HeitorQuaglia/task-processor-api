from pydantic import BaseModel, Field
from typing import Optional, Literal, Union


class UrlTaskData(BaseModel):
    url: str = Field(..., description="URL a ser validada")


class CsvTaskData(BaseModel):
    file_url: str = Field(..., description="URL do arquivo CSV no S3")
    column_name: str = Field(..., description="Nome da coluna a ser processada no CSV")


class TaskResult(BaseModel):
    task_id: str = Field(..., description="ID único da tarefa")
    type: Literal["url", "csv"] = Field(..., description="Tipo da tarefa: 'url' ou 'csv'")
    status: Literal["processing", "error", "completed"] = Field(..., description="Status da tarefa")
    result: Optional[float | str] = Field(None, description="Resultado numérico (para CSV) ou string (para URL)")
    comment: Optional[str] = Field(None, description="Comentário detalhado sobre o resultado")
    task_data: Union[UrlTaskData, CsvTaskData] = Field(..., description="Dados específicos da tarefa")

    class Config:
        orm_mode = True
