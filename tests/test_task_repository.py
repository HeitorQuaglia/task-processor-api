# File: tests/test_task_repository.py

from unittest.mock import AsyncMock, patch

import pytest
from app.models.task_result import TaskResult
from app.repositories.task_repository import TaskRepository


@pytest.mark.asyncio
async def test_save_task():
    task_data = TaskResult(
        task_id="test_task_id",
        type="url",
        status="processing",
        result=None,
        comment=None,
        task_metadata={"url": "http://example.com"}
    )

    mock_collection = AsyncMock()
    with patch(
            "app.repositories.task_repository.get_mongo_collection",
            return_value=mock_collection
    ):
        repo = TaskRepository()
        await repo.save_task(task_data)

    mock_collection.insert_one.assert_awaited_once_with(task_data.dict())


@pytest.mark.asyncio
async def test_get_task_found():
    task_id = "test_task_id"
    mocked_result = {
        "task_id": task_id,
        "type": "url",
        "status": "completed",
        "result": "http://example.com",
        "comment": "Test comment",
        "task_metadata": {"url": "http://example.com"}
    }

    mock_collection = AsyncMock()
    mock_collection.find_one = AsyncMock(return_value=mocked_result)

    with patch(
            "app.repositories.task_repository.get_mongo_collection",
            return_value=mock_collection
    ):
        repo = TaskRepository()
        task = await repo.get_task(task_id)

    assert task is not None
    assert task.task_id == task_id
    assert task.dict() == mocked_result


@pytest.mark.asyncio
async def test_get_task_not_found():
    mock_collection = AsyncMock()
    mock_collection.find_one = AsyncMock(return_value=None)

    with patch(
            "app.repositories.task_repository.get_mongo_collection",
            return_value=mock_collection
    ):
        repo = TaskRepository()
        task = await repo.get_task("nonexistent_task_id")

    assert task is None


@pytest.mark.asyncio
async def test_update_task_success():
    task_data = TaskResult(
        task_id="test_task_id",
        type="url",
        status="completed",
        result="http://example.com/result",
        comment="Task completed successfully",
        task_metadata={"url": "http://example.com"}
    )

    mock_collection = AsyncMock()
    mock_collection.update_one = AsyncMock(return_value=AsyncMock(matched_count=1))

    with patch(
            "app.repositories.task_repository.get_mongo_collection",
            return_value=mock_collection
    ):
        repo = TaskRepository()
        await repo.update_task(task_data)

    mock_collection.update_one.assert_awaited_once_with(
        {"task_id": task_data.task_id},
        {"$set": task_data.dict()},
    )


@pytest.mark.asyncio
async def test_update_task_no_match():
    task_data = TaskResult(
        task_id="nonexistent_task_id",
        type="url",
        status="processing",
        result=None,
        comment=None,
        task_metadata={"url": "http://example.com"}
    )

    mock_collection = AsyncMock()
    mock_collection.update_one = AsyncMock(return_value=AsyncMock(matched_count=0))

    with patch(
            "app.repositories.task_repository.get_mongo_collection",
            return_value=mock_collection
    ):
        repo = TaskRepository()
        with pytest.raises(ValueError, match=f"No task found with task_id {task_data.task_id}."):
            await repo.update_task(task_data)

    mock_collection.update_one.assert_awaited_once_with(
        {"task_id": task_data.task_id},
        {"$set": task_data.dict()},
    )
