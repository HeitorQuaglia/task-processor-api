from pydantic import BaseModel, HttpUrl, Field, root_validator
from typing import Optional, Required


class ProcessDataInput(BaseModel):
    url: str | None = None
    column_name: str | None = None
    # column_name: Optional[str] = None
    # url: Optional[HttpUrl] = Field(None, description="URL para validar. Deve ser um link válido.")
    # column_name: Optional[str] = Field(None, min_length=1, description="Nome da coluna a ser processada no CSV.")

    # @root_validator(pre=True)
    # def validate_inputs(cls, values):
    #     url = values.get("url")
    #     column_name = values.get("column_name")
    #
    #     if not url and not column_name:
    #         raise ValueError("É necessário fornecer uma URL ou um arquivo CSV.")
    #
    #     if url and column_name:
    #         raise ValueError("Somente uma opção pode ser fornecida: URL ou arquivo CSV.")
    #
    #     return values
