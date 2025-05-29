from typing import Protocol, Any
from fastapi import BackgroundTasks

class ProcessorProtocol(Protocol):
    task_id: str
    payload: Any

    def validate(self) -> None:
        ...

    def process(self) -> None:
        ...

    def create_task_data(self) -> Any:
        ...

    def add_background_task(self, background_tasks: BackgroundTasks) -> None:
        ...

    def response(self) -> dict[str, Any]:
        ...
