import json
import os
import urllib
from typing import List

from botbuilder.core import ActivityHandler, MessageFactory, TurnContext
from botbuilder.schema import (
    ActionTypes,
    Attachment,
    CardAction,
    ChannelAccount,
    SuggestedActions,
)
from core.config import settings
from llm.assisstant import assistant_handler
from models.assistant_bot_models import FileInfo
from utils import get_logger

logger = get_logger(__name__)


class AssistantBot(ActivityHandler):
    thread_id = None
    vector_store_id = []

    async def on_members_added_activity(
        self, members_added: List[ChannelAccount], turn_context: TurnContext
    ) -> None:
        """Onboards new members to the assistant by creating a new thread and adding a initial welcome message.

        members_added (List[ChannelAccount]): The list of channel accounts.
        turn_context (TurnContext): The turn context.
        RETURNS (None): No return value.
        """
        for member in members_added:
            if member.id != turn_context.activity.recipient.id:
                # Initialize thread in assistant
                self.thread_id = assistant_handler.create_thread()

                # # Initialize vector store in assistant
                # self.vector_store_id = assistant_handler.create_vector_store(thread_id=self.thread_id)

                # Respond with welcome message
                welcome_message = (
                    "Hello and welcome! I am your personal joke assistant."
                )
                await turn_context.send_activity(welcome_message)

                # Respond with suggested actions
                suggested_topics_message = (
                    "Which topic would like to hear a joke about?"
                )
                suggested_topics = MessageFactory.text(suggested_topics_message)
                suggested_topics.suggested_actions = SuggestedActions(
                    actions=[
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
                    ]
                )
                await turn_context.send_activity(suggested_topics)

                # Add messages from assisstant to thread
                assistant_handler.send_assisstant_message(
                    message=welcome_message, thread_id=self.thread_id
                )
                assistant_handler.send_assisstant_message(
                    message=suggested_topics_message, thread_id=self.thread_id
                )

    async def on_message_activity(self, turn_context: TurnContext) -> None:
        """Acts upon new messages or attachments added to a channel.

        turn_context (TurnContext): The turn context.
        RETURNS (None): No return value.
        """
        if (
            turn_context.activity.attachments
            and len(turn_context.activity.attachments) > 0
        ):
            # Download attachment and add it to thread
            await self.__handle_incoming_attachment(turn_context)
            pass
        else:
            # Interact with assistant
            message = assistant_handler.send_user_message(
                message=turn_context.activity.text,
                thread_id=self.thread_id,
            )
            if message:
                return await turn_context.send_activity(MessageFactory.text(message))

    async def __handle_incoming_attachment(self, turn_context: TurnContext) -> None:
        """Handles all attachments uploaded by users.

        turn_context (TurnContext): The turn context.
        RETURNS (None): No return value.
        """
        for attachment in turn_context.activity.attachments:
            file_info = await self.__download_attachment_and_write(attachment)
            if file_info:
                self.vector_store_ids = assistant_handler.send_user_file(
                    file_path=file_info.file_path, thread_id=self.thread_id
                )

    async def __download_attachment_and_write(
        self, attachment: Attachment
    ) -> FileInfo | None:
        """Retrieves the attachment via the attachment's contentUrl.

        attachment (Attachment): Attachment sent by the user.
        RETURNS (dict): Returns a dic containing the attachment details including the keys 'filename' and 'local_path'.
        """
        try:
            response = urllib.request.urlopen(attachment.content_url)
            headers = response.info()

            # If user uploads JSON file, this prevents it from being written as
            # "{"type":"Buffer","data":[123,13,10,32,32,34,108..."
            if headers["content-type"] == "application/json":
                data = bytes(json.load(response)["data"])
            else:
                data = response.read()

            # Define directory
            directory_path = os.path.join(settings.HOME_DIRECTORY, self.thread_id)
            file_path = os.path.join(directory_path, attachment.name)
            if not os.path.exists(directory_path):
                os.makedirs(directory_path)

            # Write file
            with open(file_path, "wb") as file:
                file.write(data)

            return FileInfo(
                file_name=attachment.name,
                file_path=file_path,
            )
        except Exception as e:
            logger.error(f"Failed to download file '{attachment.name}'", e)
            return None
