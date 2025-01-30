from io import BytesIO
from unittest.mock import patch, AsyncMock

import pytest
from fastapi import BackgroundTasks, HTTPException, UploadFile
from starlette.datastructures import Headers
from botocore.exceptions import ClientError

from app.models.process_data_input import ProcessDataInput
from app.services.mongo_service import MongoService
from app.services.processor_service import ProcessorService
from app.services.task_service import TaskService


@pytest.mark.asyncio
@patch.object(MongoService, "save_task", new_callable=AsyncMock)
@patch.object(TaskService, "validate_url", new_callable=AsyncMock)
async def test_process_valid_url(mock_validate_url, mock_save_task):
    background_tasks = BackgroundTasks()

    payload = ProcessDataInput(url = "https://www.google.com")

    response = await ProcessorService.process_data(background_tasks, payload)

    for task in background_tasks.tasks:
        await task()

    assert response["url"] == payload.url
    assert response["message"] == "Processando validação de URL"
    assert "task_id" in response

    mock_validate_url.assert_called_once()
    mock_save_task.assert_awaited_once()


@pytest.mark.asyncio
@patch.object(MongoService, "save_task", new_callable=AsyncMock)
@patch.object(TaskService, "validate_url", new_callable=AsyncMock)
async def test_process_invalid_url(mock_validate_url, mock_save_task):
    background_tasks = BackgroundTasks()
    payload = ProcessDataInput(url="invalid-url")

    with pytest.raises(HTTPException) as exc:
        await ProcessorService.process_data(background_tasks, payload)

    assert exc.value.status_code == 400
    assert "URL fornecida é inválida." in exc.value.detail

    mock_save_task.assert_not_called()
    mock_validate_url.assert_not_called()

@pytest.mark.asyncio
@patch.object(MongoService, "save_task", new_callable=AsyncMock)
@patch.object(TaskService, "process_csv", new_callable=AsyncMock)
@patch("app.services.processor_service.upload_to_s3", return_value="https://s3.fake-bucket.com/sample.csv")
async def test_process_csv_success(mock_upload_to_s3, mock_process_csv, mock_save_task):
    background_tasks = BackgroundTasks()
    file_content = BytesIO(b"col1,col2,col3\n1,2,3\n4,5,6")
    headers = Headers({"content-type": "text/csv"})
    file = UploadFile(filename="sample.csv", file=file_content, headers=headers)

    payload = ProcessDataInput(column="1", file=file)

    response = await ProcessorService.process_data(background_tasks, payload)

    for task in background_tasks.tasks:
        await task()

    assert response["file_url"] == "https://s3.fake-bucket.com/sample.csv"
    assert response["message"] == "Processando CSV..."
    assert "task_id" in response

    mock_upload_to_s3.assert_called_once()
    mock_process_csv.assert_called_once_with(response["task_id"], response["file_url"], int(payload.column))
    mock_save_task.assert_awaited_once()

@pytest.mark.asyncio
@patch.object(MongoService, "save_task", new_callable=AsyncMock)
@patch.object(TaskService, "process_csv", new_callable=AsyncMock)
async def test_invalid_file_format(mock_process_csv, mock_save_task):
    background_tasks = BackgroundTasks()

    file_content = BytesIO(b"\x89PNG\r\n\x1a\n\x00\x00\x00")
    headers = Headers({"content-type": "image/png"})  # Simulando um arquivo de imagem
    file = UploadFile(filename="invalid.png", file=file_content, headers=headers)

    payload = ProcessDataInput(column="1", file=file)

    with pytest.raises(HTTPException) as exc:
        await ProcessorService.process_data(background_tasks, payload)

    assert exc.value.status_code == 400
    assert "Arquivo inválido. Apenas arquivos CSV são aceitos." in exc.value.detail

    mock_save_task.assert_not_called()
    mock_process_csv.assert_not_called()

@pytest.mark.asyncio
@patch("app.services.processor_service.upload_to_s3", side_effect=ClientError({"Error": {"Code": "500"}}, "PutObject"))  # Mockando erro no S3
@patch.object(MongoService, "save_task", new_callable=AsyncMock)
@patch.object(TaskService, "process_csv", new_callable=AsyncMock)
async def test_s3_upload_failure(mock_process_csv, mock_save_task, mock_upload_to_s3):
    background_tasks = BackgroundTasks()

    file_content = BytesIO(b"col1,col2,col3\n1,2,3\n4,5,6")
    headers = Headers({"content-type": "text/csv"})
    file = UploadFile(filename="sample.csv", file=file_content, headers=headers)

    payload = ProcessDataInput(column="1", file=file)

    with pytest.raises(HTTPException) as exc:
        await ProcessorService.process_data(background_tasks, payload)

    assert exc.value.status_code == 503
    assert "Erro ao fazer upload do arquivo para o S3." in exc.value.detail

    mock_save_task.assert_not_called()
    mock_process_csv.assert_not_called()
    mock_upload_to_s3.assert_called_once_with(file)

@pytest.mark.asyncio
@patch("app.services.processor_service.upload_to_s3", side_effect=Exception("Erro desconhecido!"))
@patch.object(MongoService, "save_task", new_callable=AsyncMock)
@patch.object(TaskService, "process_csv", new_callable=AsyncMock)
async def test_unexpected_processing_error(mock_process_csv, mock_save_task, mock_upload_to_s3):
    background_tasks = BackgroundTasks()

    # Criar um arquivo CSV válido
    file_content = BytesIO(b"col1,col2,col3\n1,2,3\n4,5,6")
    headers = Headers({"content-type": "text/csv"})
    file = UploadFile(filename="sample.csv", file=file_content, headers=headers)

    payload = ProcessDataInput(column="1", file=file)

    with pytest.raises(HTTPException) as exc:
        await ProcessorService.process_data(background_tasks, payload)

    assert exc.value.status_code == 500
    assert "Erro inesperado ao tentar processar o arquivo." in exc.value.detail

    mock_save_task.assert_not_called()
    mock_process_csv.assert_not_called()
    mock_upload_to_s3.assert_called_once_with(file)
