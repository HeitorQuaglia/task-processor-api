from celery import Celery
import os

CELERY_BROKER_URL = os.getenv("CELERY_BROKER_URL", "amqp://guest:guest@rabbitmq:5672//")
# CELERY_BACKEND_URL = os.getenv("CELERY_BACKEND_URL", "redis://redis:6379/0")

celery = Celery("tasks", broker=CELERY_BROKER_URL, backend="rpc://")

celery.conf.update(
    task_routes={
        "app.tasks.worker.*": {"queue": "tasks"},
    },
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    broker_connection_retry_on_startup=True,
)

# Teste de conexão
if __name__ == "__main__":
    try:
        celery.connection().ensure_connection(max_retries=3)
        print("Celery conectado ao broker com sucesso!")
    except Exception as e:
        print(f"Erro ao conectar o Celery ao broker: {e}")
