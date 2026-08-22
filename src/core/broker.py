import taskiq_fastapi
from taskiq import SmartRetryMiddleware, TaskiqEvents, TaskiqState
from taskiq_aio_pika import AioPikaBroker, Exchange, Queue

from src.core.config import settings
from src.core.logging import setup_logging

broker = AioPikaBroker(
    settings.rabbit.RABBITMQ_URL,
    qos=1,
    exchange=Exchange(name="cafe"),
    task_queues=[Queue(name="cafe")],
    dead_letter_queue=Queue(name="cafe.dead"),
    delay_queue=Queue(name="cafe.delay"),
).with_middlewares(
    SmartRetryMiddleware(
        default_retry_count=settings.taskiq.TASKIQ_RETRY_COUNT,
        default_delay=settings.taskiq.TASKIQ_RETRY_DELAY,
        use_jitter=True,
        use_delay_exponent=True,
        max_delay_exponent=120,
    )
)

taskiq_fastapi.init(broker, "src.main:app")


@broker.on_event(TaskiqEvents.WORKER_STARTUP)
async def startup(state: TaskiqState) -> None:
    setup_logging()
