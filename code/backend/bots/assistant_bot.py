from typing import List

from botbuilder.core import ActivityHandler, MessageFactory, TurnContext
from botbuilder.schema import ChannelAccount
from llm.assisstant import assistant_handler
from botbuilder.schema import ChannelAccount, CardAction, ActionTypes, SuggestedActions


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
                welcome_message = "Hello and welcome! I am your personal joke assistant."
                await turn_context.send_activity(
                    welcome_message
                )

                # Respond with suggested actions
                suggested_topics_message = "Which topic would like to hear a joke about?"
                suggested_topics = MessageFactory.text(suggested_topics_message)
                suggested_topics.suggested_actions = SuggestedActions(actions=[
                    CardAction(
                        type=ActionTypes.im_back,
                        title="Cars",
                        text="Cars",
                        display_text="Cars",
                        value="Cars",
                    ),
                    CardAction(
                        type=ActionTypes.im_back,
                        title="Sports",
                        text="Sports",
                        display_text="Sports",
                        value="Sports",
                    ),
                    CardAction(
                        type=ActionTypes.im_back,
                        title="Atoms",
                        text="Atoms",
                        display_text="Atoms",
                        value="Atoms",
                    ),
                ])
                await turn_context.send_activity(suggested_topics)

                # Add messages from assisstant to thread
                assistant_handler.send_assisstant_message(welcome_message)
                assistant_handler.send_assisstant_message(suggested_topics_message)

    async def on_message_activity(self, turn_context: TurnContext):
        """Acts upon new messages added to a channel.

        turn_context (TurnContext): The turn context.
        RETURNS (str): The assistant message actvity is being returned.
        """
        # Interact with assistant
        message = assistant_handler.send_user_message(
            message=turn_context.activity.text,
            thread_id=self.thread_id,
        )
        if message:
            return await turn_context.send_activity(MessageFactory.text(message))
