import logging

from azure.monitor.opentelemetry import configure_azure_monitor
from core.config import settings
from opentelemetry import trace
from opentelemetry.instrumentation.aiohttp_client import AioHttpClientInstrumentor
from opentelemetry.instrumentation.aiohttp_server import AioHttpServerInstrumentor
from opentelemetry.sdk.resources import Resource


def enable_logging():
    # Configure base logger
    log_level = logging.DEBUG if settings.DEBUG else settings.LOGGING_LEVEL
    logging.basicConfig(format="%(asctime)s:%(levelname)s:%(message)s", level=log_level)

    # Configure azure monitor logs
    configure_azure_monitor(
        connection_string=settings.APPLICATIONINSIGHTS_CONNECTION_STRING,
        instrumentation_options={
            "azure_sdk": {"enabled": True},
            "django": {"enabled": False},
            "fastapi": {"enabled": False},
            "flask": {"enabled": True},
            "psycopg2": {"enabled": False},
            "requests": {"enabled": False},
            "urllib": {"enabled": False},
            "urllib3": {"enabled": False},
        },
        resource=Resource.create(
            {
                "service.name": settings.SERVER_NAME,
                "service.namespace": settings.PROJECT_NAME,
                "service.instance.id": settings.WEBSITE_INSTANCE_ID,
            }
        ),
        logger_name=settings.PROJECT_NAME,
        enable_live_metrics=True,
    )

    # Enable additional instrumentation
    AioHttpClientInstrumentor().instrument()
    AioHttpServerInstrumentor().instrument()


def get_logger(name: str) -> logging.Logger:
    logger = logging.getLogger(name=f"{settings.PROJECT_NAME}.{name}")
    if settings.DEBUG:
        logger.setLevel(logging.DEBUG)
    else:
        logger.setLevel(settings.LOGGING_LEVEL)
    return logger


def get_tracer(name: str) -> trace.Tracer:
    tracer = trace.get_tracer(name)
    return tracer
