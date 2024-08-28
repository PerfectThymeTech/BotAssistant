from aiohttp import web
from aiohttp.web import Request, Response
from botbuilder.core.integration import aiohttp_error_middleware
from botbuilder.integration.aiohttp import (
    CloudAdapter,
    ConfigurationBotFrameworkAuthentication,
)
from bots.assistant_bot import AssistantBot
from bots.utils_bot import BotUtils
from core.config import settings as CONFIG
from utils import enable_logging

# Create cloud adapter
ADAPTER = CloudAdapter(ConfigurationBotFrameworkAuthentication(CONFIG))
ADAPTER.on_turn_error = BotUtils.on_error

# Create bot
BOT = AssistantBot()

# Create app
APP = web.Application(middlewares=[aiohttp_error_middleware])


# Listen for incoming requests on /api/messages
async def messages(req: Request) -> Response:
    return await ADAPTER.process(req, BOT)


# Add route to app
APP.router.add_post("/api/messages", messages)

# Enable logging
enable_logging()


if __name__ == "__main__":
    try:
        web.run_app(APP, host="localhost", port=CONFIG.PORT)
    except Exception as error:
        raise error
