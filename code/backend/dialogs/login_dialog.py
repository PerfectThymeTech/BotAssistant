from botbuilder.core import BotFrameworkAdapter, UserState
from botbuilder.dialogs import (
    ComponentDialog,
    DialogTurnResult,
    WaterfallDialog,
    WaterfallStepContext,
)
from botbuilder.dialogs.dialog_context import DialogContext
from botbuilder.dialogs.prompts import ConfirmPrompt, OAuthPrompt, OAuthPromptSettings
from botbuilder.schema import ActivityTypes
from models.assistant_bot_models import UserData
from utils import get_logger

logger = get_logger(__name__)


class LoginDialog(ComponentDialog):
    def __init__(self, connection_name: str, user_state: UserState) -> None:
        """Initailizes the login dialog.

        connection_name (str): Specifies the connection name.
        RETURNS (None): No return value.
        """
        super(LoginDialog, self).__init__(dialog_id=LoginDialog.__name__)

        # Configure initial dialog id
        self.initial_dialog_id = "WaterfallDialog"
        self.connection_name = connection_name

        # Configure user state
        if user_state is None:
            raise TypeError(
                "Missing user state parameter. 'user_state' is required but None was given."
            )
        self.user_state = user_state
        self.user_state_accessor = self.user_state.create_property("UserData")

        # COnfigure dialog
        self.add_dialog(
            dialog=OAuthPrompt(
                dialog_id=OAuthPrompt.__name__,
                settings=OAuthPromptSettings(
                    connection_name=connection_name,
                    text="Please sign in.",
                    title="Sign In",
                    timeout=300000,
                ),
            )
        )

        self.add_dialog(
            dialog=ConfirmPrompt(
                dialog_id=ConfirmPrompt.__name__,
            ),
        )

        self.add_dialog(
            dialog=WaterfallDialog(
                dialog_id=self.initial_dialog_id,
                steps=[
                    self.prompt_step,
                    self.login_step,
                ],
            )
        )

    async def on_begin_dialog(
        self, inner_dc: DialogContext, options: object
    ) -> DialogTurnResult:
        """Called when the dialog is started and pushed onto the parent's dialog stack.

        inner_dc (DialogContext): Inner dialog context within the dialog.
        options (object): Options for the internal
        RETURNS (DialogTurnResult): Dialog step result.
        """
        result = await self.__interrupt(inner_dc=inner_dc)
        if result:
            return result
        return await super().on_begin_dialog(inner_dc=inner_dc, options=options)

    async def on_continue_dialog(self, inner_dc: DialogContext) -> DialogTurnResult:
        """Called when the dialog is continued.

        inner_dc (DialogContext): Inner dialog context within the dialog.
        RETURNS (DialogTurnResult): Dialog step result.
        """
        result = await self.__interrupt(inner_dc=inner_dc)
        if result:
            return result
        return await super().on_continue_dialog(inner_dc=inner_dc)

    async def prompt_step(self, step_context: WaterfallStepContext) -> DialogTurnResult:
        """Handles the prompt step of the login dialog.

        step_context (WaterfallStepContext): Specifies the step context within the waterfall dialog.
        RETURNS (DialogTurnResult): Returns the dialog result of this step.
        """
        logger.info("Running prompt step in login dialog.")
        return await step_context.begin_dialog(dialog_id=OAuthPrompt.__name__)

    async def login_step(self, step_context: WaterfallStepContext) -> DialogTurnResult:
        """Handles the login step of the login dialog.

        step_context (WaterfallStepContext): Specifies the step context within the waterfall dialog.
        RETURNS (DialogTurnResult): Returns the dialog result of this step.
        """
        logger.info("Running login step in login dialog.")

        logger.info("Loading user data.")
        user_data: UserData = await self.user_state_accessor.get(
            step_context.context, UserData
        )

        if step_context.result:
            logger.info(f"Successful login.")
            logger.debug(f"Successful login with token: '{step_context.result.token}'.")
            user_data.login_succeeded = True
            await step_context.context.send_activity(
                "Thank you! You have successfully logged in."
            )

        else:
            logger.info(f"Unsuccessful login.")
            user_data.login_succeeded = False
            await step_context.context.send_activity(
                "I am sorry! Login was not successful. Please try again."
            )
        return await step_context.end_dialog()

    async def __interrupt(self, inner_dc: DialogContext) -> DialogTurnResult:
        """Called when the dialog is started and pushed onto the parent's dialog stack.

        inner_dc (DialogContext): Inner dialog context within the dialog.
        RETURNS (DialogTurnResult): Dialog step result.
        """
        result = None
        if inner_dc.context.activity.type == ActivityTypes.message:
            text = inner_dc.context.activity.text.lower().strip()

            if text == "logout":
                bot_adapter: BotFrameworkAdapter = inner_dc.context.adapter
                await bot_adapter.sign_out_user(
                    context=inner_dc.context, connection_name=self.connection_name
                )
                await inner_dc.context.send_activity(
                    "You have been successfully signed out. Goodbye. See you soon."
                )
                result = await inner_dc.cancel_all_dialogs()
        return result
