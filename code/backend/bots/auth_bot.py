from typing import List

from botbuilder.core import ConversationState, TurnContext, UserState
from botbuilder.dialogs import Dialog
from botbuilder.schema import ChannelAccount
from bots.assistant_bot import AssistantBot
from dialogs.dialog_helper import DialogHelper


class AuthBot(AssistantBot):
    def __init__(
        self,
        conversation_state: ConversationState,
        user_state: UserState,
        dialog: Dialog,
    ) -> None:
        super(AuthBot, self).__init__(conversation_state, user_state)
        self.dialog = dialog

    async def on_members_added_activity(
        self, members_added: List[ChannelAccount], turn_context: TurnContext
    ) -> None:
        await super(AuthBot, self).on_members_added_activity(
            members_added, turn_context
        )
        await turn_context.send_activity("Type any message to get logged in.")

    async def on_turn(self, turn_context: TurnContext) -> None:
        await super(AuthBot, self).on_turn(turn_context)

    async def on_message_activity(self, turn_context: TurnContext) -> None:
        await super(AuthBot, self).on_message_activity(turn_context)

    async def on_token_response_event(self, turn_context: TurnContext):
        await DialogHelper.run_dialog(
            dialog=self.dialog,
            turn_context=turn_context,
            accessor=self.conversation_state_accessor,
        )

    # async def on_teams_signin_verify_state(self, turn_context: TurnContext):
    #     pass
