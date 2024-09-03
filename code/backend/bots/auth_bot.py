from typing import List
from botbuilder.schema import ChannelAccount
from bots.assistant_bot import AssistantBot
from botbuilder.core import TurnContext, UserState


class AuthBot(AssistantBot):
    def __init__(self, user_state: UserState) -> None:
        super(AuthBot, self).__init__(user_state)
    
    async def on_members_added_activity(self, members_added: List[ChannelAccount], turn_context: TurnContext) -> None:
        return await super(AuthBot, self).on_members_added_activity(members_added, turn_context)

    async def on_turn(self, turn_context: TurnContext) -> None:
        return await super(AuthBot, self).on_turn(turn_context)
    
    async def on_message_activity(self, turn_context: TurnContext) -> None:
        return await super(AuthBot, self).on_message_activity(turn_context)

    async def on_token_response_event(self, turn_context: TurnContext):
        pass

    async def on_teams_signin_verify_state(self, turn_context: TurnContext):
        pass
