"""
Pacote para serviços relacionados a manipulação de arquivos.
"""
from app.services.file.file_uploader import IFileUploader, S3FileUploader

__all__ = [
    'IFileUploader',
    'S3FileUploader',
]
