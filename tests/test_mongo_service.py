import pytest
from unittest.mock import AsyncMock, patch
from app.services.mongo_service import MongoService
from app.repositories.task_repository import TaskRepository
from app.models.task_result import TaskResult, UrlTaskData

@pytest.mark.asyncio
@patch.object(TaskRepository, "save_task", new_callable=AsyncMock)  # Mock do MongoDB
async def test_save_task_success(mock_save_task):
    task_data = TaskResult(
        task_id="12345",
        type="url",
        status="processing",
        result=None,
        comment="Processando...",
        task_metadata=UrlTaskData(url="https://example.com")
    )

    await MongoService.save_task(task_data)

    mock_save_task.assert_called_once_with(task_data)

@pytest.mark.asyncio
@patch.object(TaskRepository, "get_task", new_callable=AsyncMock)  # Mock do MongoDB
async def test_get_task_success(mock_get_task):
    task_data = TaskResult(
        task_id="12345",
        type="url",
        status="completed",
        result="valid",
        comment="URL validada com sucesso.",
        task_metadata=UrlTaskData(url="https://example.com")
    )

    mock_get_task.return_value = task_data
    result = await MongoService.get_task("12345")

    assert result == task_data

    mock_get_task.assert_called_once_with("12345")

@pytest.mark.asyncio
@patch.object(TaskRepository, "get_task", new_callable=AsyncMock)  # Mock do MongoDB
async def test_get_task_not_found(mock_get_task):
    mock_get_task.return_value = None

    result = await MongoService.get_task("non-existent-task-id")

    assert result is None

    mock_get_task.assert_called_once_with("non-existent-task-id")

@pytest.mark.asyncio
@patch.object(TaskRepository, "get_task", new_callable=AsyncMock)
@patch.object(TaskRepository, "update_task", new_callable=AsyncMock)
async def test_update_task_success(mock_update_task, mock_get_task):
    task_data = TaskResult(
        task_id="12345",
        type="url",
        status="processing",
        result=None,
        comment="Processando...",
        task_metadata=UrlTaskData(url="https://example.com")
    )

    mock_get_task.return_value = task_data

    await MongoService.update_task(task_id="12345", status="completed", result="valid", comment="URL validada.")

    updated_task = TaskResult(
        task_id=task_data.task_id,
        type=task_data.type,
        status="completed",
        result="valid",
        comment="URL validada.",
        task_metadata=task_data.task_metadata
    )

    mock_update_task.assert_called_once_with(updated_task)

    mock_get_task.assert_called_once_with("12345")

@pytest.mark.asyncio
@patch.object(TaskRepository, "get_task", new_callable=AsyncMock)
@patch.object(TaskRepository, "update_task", new_callable=AsyncMock)
async def test_update_task_not_found(mock_update_task, mock_get_task):
    mock_get_task.return_value = None

    with pytest.raises(ValueError) as exc:
        await MongoService.update_task(task_id="non-existent-task-id", status="completed", result="valid", comment="URL validada.")

    assert "Tarefa com task_id non-existent-task-id não encontrada." in str(exc.value)

    mock_update_task.assert_not_called()
    mock_get_task.assert_called_once_with("non-existent-task-id")
