import pytest
from unittest.mock import AsyncMock, patch
from app.services.task_service import TaskService
from app.services.mongo_service import MongoService

@pytest.mark.asyncio
@patch.object(MongoService, "update_task", new_callable=AsyncMock)
async def test_update_task_status_success(mock_update_task):
    await TaskService.update_task_status(task_id="12345", status="completed", result="valid", comment="URL validada.")
    mock_update_task.assert_called_once_with("12345", status="completed", result="valid", comment="URL validada.")

@pytest.mark.asyncio
@patch.object(MongoService, "update_task", new_callable=AsyncMock)
@patch("app.services.task_service.logger", new_callable=AsyncMock)
async def test_update_task_status_task_not_found(mock_logger, mock_update_task):
    mock_update_task.side_effect = ValueError("Tarefa com task_id 99999 não encontrada.")

    await TaskService.update_task_status(task_id="99999", status="error", result=None, comment="Erro inesperado.")

    mock_logger.error.assert_called_once()
    mock_update_task.assert_called_once_with("99999", status="error", result=None, comment="Erro inesperado.")

@pytest.mark.asyncio
@patch.object(MongoService, "update_task", new_callable=AsyncMock)
@patch("app.services.task_service.validate_url", return_value={"status": "completed", "result": "valid", "comment": "URL validada."})
async def test_validate_url_success(mock_validate_url, mock_update_task):
    await TaskService.validate_url(task_id="12345", url="https://example.com")

    mock_validate_url.assert_called_once_with("https://example.com")
    mock_update_task.assert_called_once_with("12345", "completed", "valid", "URL validada.")

@pytest.mark.asyncio
@patch.object(MongoService, "update_task", new_callable=AsyncMock)
@patch("app.services.task_service.validate_url", return_value={"status": "error", "result": "invalid", "comment": "Erro ao validar a URL."})
async def test_validate_url_failure(mock_validate_url, mock_update_task):
    await TaskService.validate_url(task_id="67890", url="invalid-url")

    mock_validate_url.assert_called_once_with("invalid-url")
    mock_update_task.assert_called_once_with("67890", "error", "invalid", "Erro ao validar a URL.")

@pytest.mark.asyncio
@patch.object(MongoService, "update_task", new_callable=AsyncMock)
@patch("app.services.task_service.process_csv", return_value={"status": "completed", "result": 10.5, "comment": "Média calculada."})
async def test_process_csv_success(mock_process_csv, mock_update_task):
    await TaskService.process_csv(task_id="12345", file_url="https://s3.com/sample.csv", column_index=2)

    mock_process_csv.assert_called_once_with("https://s3.com/sample.csv", 2)
    mock_update_task.assert_called_once_with("12345", "completed", 10.5, "Média calculada.")

@pytest.mark.asyncio
@patch.object(MongoService, "update_task", new_callable=AsyncMock)
@patch("app.services.task_service.process_csv", return_value={"status": "error", "result": None, "comment": "Erro ao processar o CSV."})
async def test_process_csv_failure(mock_process_csv, mock_update_task):
    await TaskService.process_csv(task_id="67890", file_url="https://s3.com/invalid.csv", column_index=5)

    mock_process_csv.assert_called_once_with("https://s3.com/invalid.csv", 5)
    mock_update_task.assert_called_once_with("67890", "error", None, "Erro ao processar o CSV.")
