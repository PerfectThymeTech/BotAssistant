from datetime import datetime

from botbuilder.core import TurnContext
from botbuilder.schema import Activity, ActivityTypes
from utils import get_logger

logger = get_logger(__name__)


class BotUtils:

    @staticmethod
    async def on_error(context: TurnContext, error: Exception):
        # Log error
        logger.error("Unexpected error within the application", error)

        # Send a message to the user
        await context.send_activity(
            "The bot encountered an error or bug. The team will get notified and look into the issue. Sorry for any inconveniences caused."
        )

        # For the Bot Framework emulator channel send a trace activity
        if context.activity.channel_id == "emulator":
            # Create a trace activity that contains the error object
            trace_activity = Activity(
                label="TurnError",
                name="on_turn_error Trace",
                timestamp=datetime.now(datetime.UTC),
                type=ActivityTypes.trace,
                value=f"{error}",
                value_type="https://www.botframework.com/schemas/error",
            )
            # Send a trace activity, which will be displayed in Bot Framework Emulator
            await context.send_activity(trace_activity)
