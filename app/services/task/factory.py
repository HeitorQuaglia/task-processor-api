"""
Factory para criar processadores de tarefas.
"""
from app.services.mongo_service import default_mongo_service
from app.services.task.interfaces import IBackgroundTaskProcessor
from app.services.task.processors import (
    BackgroundTaskProcessor,
    DefaultUrlValidator,
    DefaultCsvProcessor
)


class TaskProcessorFactory:
    """Factory para criar processadores de tarefas em background."""
    
    @staticmethod
    def create_default_processor() -> IBackgroundTaskProcessor:
        """Cria um processador de tarefas em background com implementações padrão."""
        return BackgroundTaskProcessor(
            task_service=default_mongo_service,
            url_validator=DefaultUrlValidator(),
            csv_processor=DefaultCsvProcessor()
        )
