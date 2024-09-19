import json
import time
from typing import List

from azure.identity import DefaultAzureCredential, get_bearer_token_provider
from core.config import settings
from models.assistant_models import AttachmentResult
from openai import AzureOpenAI, BadRequestError
from openai.types.beta.threads import Run
from utils import get_logger

logger = get_logger(__name__)


class AssistantHandler:
    def __init__(
        self,
        *args,
    ) -> None:
        token_provider = get_bearer_token_provider(
            DefaultAzureCredential(
                managed_identity_client_id=settings.MANAGED_IDENTITY_CLIENT_ID
            ),
            "https://cognitiveservices.azure.com/.default",
        )
        self.client = AzureOpenAI(
            api_version=settings.AZURE_OPEN_AI_API_VERSION,
            azure_endpoint=settings.AZURE_OPEN_AI_ENDPOINT,
            azure_ad_token_provider=token_provider,
        )
        if settings.AZURE_OPENAI_ASSISTANT_ID:
            self.assistant_id = settings.AZURE_OPENAI_ASSISTANT_ID
        else:
            self.assistant_id = self.__init_assistant()

    def __init_assistant(self) -> str:
        """Creates an assistant if no assistant id was provided.

        RETURNS (str): Assistant id of the newly created assistant.
        """
        assistant = self.client.beta.assistants.create(
            name=settings.PROJECT_NAME,
            instructions=settings.AZURE_OPENAI_SYSTEM_PROMPT,
            tools=[{"type": "file_search"}],
            model=settings.AZURE_OPENAI_MODEL_NAME,
        )
        logger.info(f"Created new assisstant with assistant id: '{assistant.id}'")
        return assistant.id

    def create_thread(self) -> str:
        """Create a thread in the assistant.

        RETURNS (str): Thread id of the newly created thread.
        """
        thread = self.client.beta.threads.create(
            # tool_resources={"file_search": {"vector_store_ids": []}},
        )
        logger.debug(f"Created thread with thread id: '{thread.id}'")
        return thread.id

    def create_vector_store(self, thread_id: str) -> str:
        """Create a vector store in the assistant.

        RETURNS (str): Vector store id of the newly created vector store.
        """
        vector_store = self.client.beta.vector_stores.create(name=thread_id)
        logger.debug(f"Created vector store with id: '{vector_store.id}'")
        return vector_store.id

    def send_user_message(self, message: str, thread_id: str) -> str | None:
        """Send a message to the thread and return the response from the assistant.

        message (str): The message to be sent to the assistant.
        thread_id (str): The thread id to which the message should be sent to the assistant.
        RETURNS (str): The response from the assistant is being returned.
        """
        logger.debug(
            f"Adding message to thread with thread id: '{thread_id}' - Message (user): '{message}'"
        )
        if thread_id is None:
            return None

        message = self.client.beta.threads.messages.create(
            thread_id=thread_id,
            content=message,
            role="user",
        )

        run = self.client.beta.threads.runs.create(
            thread_id=thread_id,
            assistant_id=self.assistant_id,
        )
        run = self.__wait_for_run(run=run, thread_id=thread_id)
        run = self.__check_for_tools(run=run, thread_id=thread_id)
        response = self.__get_assisstant_response(thread_id=thread_id)

        return response

    def send_assisstant_message(self, message: str, thread_id: str) -> str | None:
        """Send a message to the thread in the context of the assisstant.

        message (str): The message to be sent to the thread in the contex of the assisstant.
        thread_id (str): The thread id to which the message should be sent to the assistant.
        RETURNS (None): No return value.
        """
        logger.debug(
            f"Adding message to thread with thread id: '{thread_id}' - Message (assistant): '{message}'"
        )
        if thread_id is None:
            return None

        _ = self.client.beta.threads.messages.create(
            thread_id=thread_id,
            content=message,
            role="assistant",
        )

    def send_user_file(self, file_path: str, thread_id: str) -> AttachmentResult:
        """Send a file to the thread in the context of the user and add it to the internal vector store.

        file_path (str): The file path to the file that should be added to the fiel search.
        thread_id (str): The thread id to which the message should be sent to the assistant.
        RETURNS (AttachmentResult): Returns the list of vector indexes and an indicator specifying whether adding the file was successful.
        """
        # Upload file
        logger.info(f"Uploading file '{file_path}' to assistant.")
        file = self.client.files.create(
            file=open(file_path, "rb"),
            purpose="assistants",
        )
        # Attach file to thread
        logger.info(f"Adding file '{file_path}' to thread '{thread_id}'")
        try:
            _ = self.client.beta.threads.messages.create(
                thread_id=thread_id,
                content="File shared by the user.",
                attachments=[{"file_id": file.id, "tools": [{"type": "file_search"}]}],
                role="user",
            )

            # Get vector store id's
            logger.debug(f"Get thread '{thread_id}'")
            thread = self.client.beta.threads.retrieve(
                thread_id=thread_id,
            )
            vector_store_ids = thread.tool_resources.file_search.vector_store_ids
            logger.debug(
                f"Vector indexes of thread '{thread_id}' are the following: '{vector_store_ids}'"
            )

            result = AttachmentResult(success=True, vector_store_ids=vector_store_ids)
        except BadRequestError as e:
            logger.error(f"Could not add file '{file_path}' to the thread.", exc_info=e)

            result = AttachmentResult(success=False, vector_store_ids=[])

        # Return result
        return result

    def __wait_for_run(self, run: Run, thread_id: str) -> Run:
        """Wait for the run to complete and return the run once completed.

        run (Run): The run object of the assistant.
        thread_id (str): The thread id to which the message should be sent to the assistant.
        RETURNS (Run): The run that completed is being returned.
        """
        while run.status not in ["completed", "cancelled", "expired", "failed"]:
            time.sleep(0.5)
            run = self.client.beta.threads.runs.retrieve(
                thread_id=thread_id, run_id=run.id
            )
            status = run.status
            logger.debug(f"Status of run '{run.id}' in thread '{thread_id}': {status}")
        return run

    def __check_for_tools(self, run: Run, thread_id: str) -> Run:
        """Acts upon tools configured for the assistant. Runs the thread afterwards and returns the completed run.

        run (Run): The run object of the assistant.
        thread_id (str): The thread id to which the message should be sent to the assistant.
        RETURNS (Run): The run that completed is being returned.
        """
        if run.required_action:
            pass

            # Do Action for Function and restart run after submitting action
            # run = self.wait_for_run(run=run, thread_id=thread_id)
        return run

    def __get_assisstant_response(self, thread_id: str) -> str:
        """Gets the latest response from the assistant thread.

        thread_id (str): The thread id from which the latest message should be fetched.
        RETURNS (str): The latest message from the assistant in the thread.
        """
        # Get message list and load as json object
        messages = self.client.beta.threads.messages.list(
            thread_id=thread_id,
        )
        messages_json = json.loads(messages.model_dump_json())

        # Extract message from json object
        message_data_0 = messages_json.get(
            "data", [{"content": [{"text": {"value": ""}}]}]
        ).pop(0)
        message_data_0_content_0 = message_data_0.get(
            "content", [{"text": {"value": ""}}]
        ).pop(0)
        first_message_text = message_data_0_content_0.get("text", {"value": ""}).get(
            "value"
        )
        logger.debug(
            f"Response from Assistant in thread '{thread_id}': {first_message_text}"
        )

        return first_message_text


assistant_handler = AssistantHandler()
