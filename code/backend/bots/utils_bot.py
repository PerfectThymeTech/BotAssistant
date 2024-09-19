from datetime import datetime

from botbuilder.core import TurnContext
from botbuilder.schema import Activity, ActivityTypes
from utils import get_logger

logger = get_logger(__name__)


class BotUtils:

    @staticmethod
    async def on_error(turn_context: TurnContext, error: Exception) -> None:
        """Handles errors in the bot.

        turn_context (TurnContext): The turn context.
        error (Exception): The exception in the bot framework.
        RETURNS (None): No return value.
        """
        # Log error
        logger.error("Unexpected error within the application", exc_info=error)

        # Send a message to the user
        await turn_context.send_activity(
            "The bot encountered an error or bug. The team will get notified and look into the issue. Sorry for any inconveniences caused."
        )

        # For the Bot Framework emulator channel send a trace activity
        if turn_context.activity.channel_id == "emulator":
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
            await turn_context.send_activity(trace_activity)
