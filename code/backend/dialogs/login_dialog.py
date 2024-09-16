from botbuilder.dialogs import (
    DialogTurnResult,
    PromptOptions,
    WaterfallDialog,
    WaterfallStepContext,
)
from botbuilder.dialogs.prompts import ConfirmPrompt, OAuthPrompt, OAuthPromptSettings
from dialogs.logout_dialog import LogoutDialog
from utils import get_logger

logger = get_logger(__name__)


class LoginDialog(LogoutDialog):
    def __init__(self, connection_name: str) -> None:
        """Initailizes the login dialog.

        connection_name (str): Specifies the connection name.
        RETURNS (None): No return value.
        """
        super(LoginDialog, self).__init__(
            dialog_id=LoginDialog.__name__, connection_name=connection_name
        )

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
                dialog_id="WaterfallDialog",
                steps=[
                    self.prompt_step,
                    self.login_step,
                ],
            )
        )

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
        if step_context.result:
            logger.info(f"Successful login.")
            logger.debug(f"Successful login with token: '{step_context.result.token}'.")
            await step_context.context.send_activity(
                "Thank you! You have successfully logged in."
            )
        else:
            logger.info(f"Unsuccessful login.")
            await step_context.context.send_activity(
                "I am sorry! Login was not successful. Please try again."
            )
        return await step_context.end_dialog()
