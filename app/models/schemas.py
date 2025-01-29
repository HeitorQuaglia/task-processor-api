from pydantic import BaseModel, HttpUrl, Field
from typing import Optional

class ProcessDataInput(BaseModel):
    url: Optional[HttpUrl] = Field(None, description="URL para validar, se fornecido")
    column_name: Optional[str] = Field(None, description="Nome da coluna a ser processada no CSV")