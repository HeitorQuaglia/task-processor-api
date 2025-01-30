from fastapi import UploadFile
from pydantic import BaseModel, root_validator
from typing import Optional


class ProcessDataInput(BaseModel):
    url: Optional[str] = None
    column: Optional[str] = None
    file: Optional[UploadFile] = None

    @root_validator(pre=True)
    def validate_inputs(cls, values):
        url = values.get("url")
        column = values.get("column")
        file = values.get("file")

        if not url and (not column or not file):
            raise ValueError("É necessário fornecer uma URL ou um arquivo CSV.")

        if url and (column or file):
            raise ValueError("Somente uma opção pode ser fornecida: URL ou arquivo CSV.")

        if file and not column:
            raise ValueError("É necessário fornecer uma coluna para o arquivo CSV.")

        if column and not column.isdigit():
            raise ValueError("'column' deve ser um numeral válido.")

        return values
