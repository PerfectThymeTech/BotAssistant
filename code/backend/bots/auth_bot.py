from typing import List

from botbuilder.core import ConversationState, TurnContext, UserState
from botbuilder.dialogs import Dialog
from botbuilder.schema import ChannelAccount
from bots.assistant_bot import AssistantBot
from dialogs.dialog_helper import DialogHelper
from models.assistant_bot_models import UserData
from utils import get_logger

logger = get_logger(__name__)


class AuthBot(AssistantBot):
    def __init__(
        self,
        conversation_state: ConversationState,
        user_state: UserState,
        login_dialog: Dialog,
    ) -> None:
        """Initailizes the Bot with states.

        conversation_state (ConversationState): Conversation state accessor.
        user_state (UserState): User state accessor.
        RETURNS (None): No return value.
        """
        super(AuthBot, self).__init__(conversation_state, user_state)
        self.login_dialog = login_dialog

    async def on_members_added_activity(
        self, members_added: List[ChannelAccount], turn_context: TurnContext
    ) -> None:
        """Onboards new members to the assistant by calling the parent bot.

        members_added (List[ChannelAccount]): The list of channel accounts.
        turn_context (TurnContext): The turn context.
        RETURNS (None): No return value.
        """
        await super(AuthBot, self).on_members_added_activity(
            members_added, turn_context
        )

    async def on_turn(self, turn_context: TurnContext) -> None:
        """Called by the adapter to handle activities.

        turn_context (TurnContext): The turn context.
        RETURNS (None): No return value.
        """
        await super(AuthBot, self).on_turn(turn_context)

    async def on_message_activity(self, turn_context: TurnContext) -> None:
        """Acts upon new messages or attachments added to a channel.

        turn_context (TurnContext): The turn context.
        RETURNS (None): No return value.
        """        
        # Access user data
        logger.info(f"Getting user data")
        user_data: UserData = await self.user_state_accessor.get(turn_context, UserData)

        if not user_data.login_succeeded:
            logger.info(f"Starting dialog to handle login.")
            await DialogHelper.run_dialog(
                dialog=self.login_dialog,
                turn_context=turn_context,
                accessor=self.conversation_state_accessor,
            )
        else:
            await super(AuthBot, self).on_message_activity(turn_context)

    async def on_token_response_event(self, turn_context: TurnContext):
        """Invoked when a tokens/response event is received.

        turn_context (TurnContext): The turn context.
        RETURNS (None): No return value.
        """
        logger.info("Token Reponse event received. Starting dialog to handle login.")
        await DialogHelper.run_dialog(
            dialog=self.login_dialog,
            turn_context=turn_context,
            accessor=self.conversation_state_accessor,
        )

    # async def on_teams_signin_verify_state(self, turn_context: TurnContext):
    #     pass
