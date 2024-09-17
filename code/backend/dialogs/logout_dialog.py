from botbuilder.core import BotFrameworkAdapter
from botbuilder.dialogs import ComponentDialog
from botbuilder.dialogs.dialog_context import DialogContext
from botbuilder.dialogs.dialog_turn_result import DialogTurnResult
from botbuilder.schema import ActivityTypes


class LogoutDialog(ComponentDialog):
    def __init__(self, dialog_id: str, connection_name: str):
        """Initailizes the logout dialog.

        connection_name (str): Specifies the connection name.
        RETURNS (None): No return value.
        """
        super(LogoutDialog, self).__init__(dialog_id)
        self.connection_name = connection_name

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
        result = await self._interrupt(inner_dc=inner_dc)
        if result:
            return result
        return await super().on_continue_dialog(inner_dc=inner_dc)

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
