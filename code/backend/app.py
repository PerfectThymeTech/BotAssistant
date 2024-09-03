from aiohttp import web
from aiohttp.web import Request, Response
from botbuilder.core import MemoryStorage, ShowTypingMiddleware, UserState
from botbuilder.core.integration import aiohttp_error_middleware
from botbuilder.integration.aiohttp import (
    CloudAdapter,
    ConfigurationBotFrameworkAuthentication,
)
from bots.assistant_bot import AssistantBot
from bots.utils_bot import BotUtils
from core.config import settings as CONFIG
from utils import enable_logging

# Enable logging
enable_logging()

# Create cloud adapter with middleware
ADAPTER = CloudAdapter(ConfigurationBotFrameworkAuthentication(CONFIG))
ADAPTER.on_turn_error = BotUtils.on_error
ADAPTER.use(ShowTypingMiddleware(delay=0.5, period=2))

# Create MemoryStorage and state
MEMORY = MemoryStorage()
USER_STATE = UserState(storage=MEMORY)

# Create bot
BOT = AssistantBot(user_state=USER_STATE)

# Create app
APP = web.Application(middlewares=[aiohttp_error_middleware])


# Listen for incoming requests on /api/messages
async def messages(req: Request) -> Response:
    return await ADAPTER.process(req, BOT)


# Add route to app
APP.router.add_post("/api/messages", messages)

if __name__ == "__main__":
    try:
        web.run_app(APP, host="localhost", port=CONFIG.PORT)
    except Exception as error:
        raise error
