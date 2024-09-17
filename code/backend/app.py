from aiohttp import web
from aiohttp.web import Request, Response
from botbuilder.azure import CosmosDbPartitionedConfig, CosmosDbPartitionedStorage
from botbuilder.core import (
    ConversationState,
    MemoryStorage,
    ShowTypingMiddleware,
    UserState,
)
from botbuilder.core.inspection import InspectionMiddleware, InspectionState
from botbuilder.core.integration import aiohttp_error_middleware
from botbuilder.integration.aiohttp import (
    CloudAdapter,
    ConfigurationBotFrameworkAuthentication,
)
from botframework.connector.auth import MicrosoftAppCredentials
from bots.assistant_bot import AssistantBot
from bots.auth_bot import AuthBot
from bots.utils_bot import BotUtils
from core.config import settings as CONFIG
from dialogs.login_dialog import LoginDialog
from utils import enable_logging

# Enable logging
enable_logging()

# Create storage and state
STORAGE = MemoryStorage()
# STORAGE = CosmosDbPartitionedStorage(
#     config=CosmosDbPartitionedConfig(
#         cosmos_db_endpoint=CONFIG.AZURE_COSMOS_ENDPOINT,
#         auth_key=CONFIG.AZURE_COSMOS_KEY,
#         database_id=CONFIG.AZURE_COSMOS_DATABASE_ID,
#         container_id=CONFIG.AZURE_COSMOS_CONTAINER_ID,
#         cosmos_client_options=None,
#         container_throughput=None,
#         key_suffix="",
#         compatibility_mode=False,
#     )
# )
USER_STATE = UserState(storage=STORAGE)
CONVERSATION_STATE = ConversationState(storage=STORAGE)  # MemoryStorage())

# Create cloud adapter with middleware
ADAPTER = CloudAdapter(ConfigurationBotFrameworkAuthentication(CONFIG))
ADAPTER.on_turn_error = BotUtils.on_error
ADAPTER.use(ShowTypingMiddleware(delay=0.1, period=2))

# Add inspection middleware for debugging
if CONFIG.DEBUG:
    INSPECTION_MIDDLEWARE = InspectionMiddleware(
        inspection_state=InspectionState(STORAGE),
        user_state=USER_STATE,
        conversation_state=None,
        credentials=MicrosoftAppCredentials(
            app_id=CONFIG.APP_ID,
            password=CONFIG.APP_PASSWORD,
            channel_auth_tenant=CONFIG.APP_TENANTID,
        ),
    )
    ADAPTER.use(INSPECTION_MIDDLEWARE)

# Create dialog
DIALOG = LoginDialog(connection_name=CONFIG.OAUTH_CONNECTION_NAME)

# Create bot
# BOT = AssistantBot(user_state=USER_STATE)
BOT = AuthBot(
    conversation_state=CONVERSATION_STATE, user_state=USER_STATE, dialog=DIALOG
)

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
