import json
import time

from azure.identity import DefaultAzureCredential, get_bearer_token_provider
from core.config import settings
from openai import AzureOpenAI
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
            tools=[],
            model=settings.AZURE_OPENAI_MODEL_NAME,
        )
        logger.info(f"Created new assisstant with assistant id: '{assistant.id}'")
        return assistant.id

    def create_thread(self) -> str:
        """Create a thread in the assistant.

        RETURNS (str): Thread id of the newly created thread.
        """
        thread = self.client.beta.threads.create()
        logger.debug(f"Created thread with thread id: '{thread.id}'")
        return thread.id

    def send_message(self, message: str, thread_id: str) -> str | None:
        """Send a message to the thread and return the response from the assistant.

        message (str): The message to be sent to the assistant.
        thread_id (str): The thread id to which the message should be sent to the assistant.
        RETURNS (str): The response from the assistant is being returned.
        """
        logger.debug(
            f"Adding message to thread with thread id: '{thread_id}' - Mesage: '{message}'"
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
        message = self.__get_assisstant_response(thread_id=thread_id)

        return message

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
