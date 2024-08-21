from typing import List

from botbuilder.core import ActivityHandler, MessageFactory, TurnContext
from botbuilder.schema import ChannelAccount
from llm.assisstant import assistant_handler


class AssistantBot(ActivityHandler):
    thread_id = None

    async def on_members_added_activity(
        self, members_added: List[ChannelAccount], turn_context: TurnContext
    ):
        """Onboards new members to the assistant by creating a new thread and adding a initial welcome message.

        members_added (List[ChannelAccount]): The list of channel accounts.
        turn_context (TurnContext): The turn context.
        RETURNS (str): The welcome message actvity is being returned.
        """
        for member in members_added:
            if member.id != turn_context.activity.recipient.id:
                # Initialize thread in assistant
                self.thread_id = assistant_handler.create_thread()
                # Respond with welcome message
                await turn_context.send_activity(
                    "Hello and welcome! I am your personal joke assistant. How can I help you today?"
                )

    async def on_message_activity(self, turn_context: TurnContext):
        """Acts upon new messages added to a channel.

        turn_context (TurnContext): The turn context.
        RETURNS (str): The assistant message actvity is being returned.
        """
        # Interact with assistant
        message = assistant_handler.send_message(
            message=turn_context.activity.text,
            thread_id=self.thread_id,
        )
        if message:
            return await turn_context.send_activity(MessageFactory.text(message))
