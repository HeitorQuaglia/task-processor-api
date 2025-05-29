import logging

from app.services.task.factory import TaskProcessorFactory
from app.services.task.interfaces import IBackgroundTaskProcessor

logger = logging.getLogger(__name__)

# Instância default para uso legado
TaskService: IBackgroundTaskProcessor = TaskProcessorFactory.create_default_processor()