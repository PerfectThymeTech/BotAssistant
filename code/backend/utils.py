from botbuilder.core.telemetry_logger_middleware import TelemetryLoggerMiddleware
from botbuilder.applicationinsights import ApplicationInsightsTelemetryClient
from botbuilder.integration.applicationinsights.aiohttp import (
    AiohttpTelemetryProcessor,
)
from core.config import settings


def get_bot_telemetry_middleware() -> ApplicationInsightsTelemetryClient:
    # Configure bot telemetry client
    telemetry_client = ApplicationInsightsTelemetryClient(
        instrumentation_key=settings.APPLICATIONINSIGHTS_INSTRUMENTATION_KEY,
        telemetry_processor=AiohttpTelemetryProcessor(),
        client_queue_size=10,
    )

    # Configure bot telemetry middleware
    telemetry_middleware = TelemetryLoggerMiddleware(
        telemetry_client=telemetry_client,
        log_personal_information=settings.DEBUG,
    )

    return telemetry_middleware
