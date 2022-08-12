from firstsaturdaybot.commands.user_commands import *
from firstsaturdaybot.commands.common_commads import *
from firstsaturdaybot.commands import *

from telegram.ext import (
    CommandHandler, 
    MessageHandler, 
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
