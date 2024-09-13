from botbuilder.dialogs import (
    DialogTurnResult,
    PromptOptions,
    WaterfallDialog,
    WaterfallStepContext,
)
from botbuilder.dialogs.prompts import ConfirmPrompt, OAuthPrompt, OAuthPromptSettings
from dialogs.logout_dialog import LogoutDialog


class LoginDialog(LogoutDialog):
    def __init__(self, connection_name: str) -> None:
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
        return await step_context.begin_dialog(dialog_id=OAuthPrompt.__name__)

    async def login_step(self, step_context: WaterfallStepContext) -> DialogTurnResult:
        if step_context.result:
            await step_context.context.send_activity(
                "Thank you! You have successfully logged in."
            )
        else:
            await step_context.context.send_activity(
                "I am sorry! Login was not successful. Please try again."
            )
        return await step_context.end_dialog()
