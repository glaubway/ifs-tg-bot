from firstsaturdaybot.commands.user_commands import (
    user_start_command
)
from firstsaturdaybot.commands.common_commads import (
    stop_nested_command,
    stop_command
)
from firstsaturdaybot.commands import (
    STOP_CONVERSATION,
    SELECTING_USER_ACTION
)
from telegram.ext import (
    CommandHandler,
    filters,
    ConversationHandler,
    CallbackQueryHandler)


user_conversation_handler = ConversationHandler(
    entry_points=[CommandHandler('start', user_start_command, filters=filters.ChatType.PRIVATE)],
    states={
        SELECTING_USER_ACTION: [
            CallbackQueryHandler(
                stop_nested_command,
                pattern="^" + str(STOP_CONVERSATION) + "$")
            ],
    },
    fallbacks=[
        CommandHandler(
            "stop",
            stop_command),
        CallbackQueryHandler(
            stop_nested_command,
            pattern=f"^{str(STOP_CONVERSATION)}$")
        ],
)
