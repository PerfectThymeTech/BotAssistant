import logging

from azure.monitor.opentelemetry import configure_azure_monitor
from opentelemetry import trace
from opentelemetry.sdk.resources import Resource
from opentelemetry.instrumentation.aiohttp_client import (
    AioHttpClientInstrumentor
)
from opentelemetry.instrumentation.aiohttp_server import AioHttpServerInstrumentor
from core.config import settings

def enable_logging():
    # Configure azure monitor logs
    configure_azure_monitor(
        connection_string=settings.APPLICATIONINSIGHTS_CONNECTION_STRING,
        instrumentation_options = {
            "azure_sdk": {"enabled": True},
            "django": {"enabled": True},
            "fastapi": {"enabled": False},
            "flask": {"enabled": True},
            "psycopg2": {"enabled": False},
            "requests": {"enabled": False},
            "urllib": {"enabled": False},
            "urllib3": {"enabled": False},
        }
        resource=Resource.create({
            "service.name": settings.SERVER_NAME,
            "service.namespace": settings.PROJECT_NAME,
            "service.instance.id": settings.WEBSITE_INSTANCE_ID,
        }),
        logger_name=__name__,
        enable_live_metrics=True,
    )

    # Enable additional instrumentation
    AioHttpClientInstrumentor().instrument()
    AioHttpServerInstrumentor().instrument()


def get_logger(name: str) -> logging.Logger:
    logger = logging.getLogger(name=name)
    if settings.DEBUG:
        logger.setLevel(logging.DEBUG)
    else:
        logger.setLevel(settings.LOGGING_LEVEL)
    return logger

def get_tracer(name: str) -> trace.Tracer:
    tracer = trace.get_tracer(name)
    return tracer
