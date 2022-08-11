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
    entry_points=[CommandHandler('start', user_start_command)],
    states={
        SELECTING_ADMIN_ACTION: [
            CallbackQueryHandler(select_user_feature, pattern="^" + str(SELECTING_ADMIN_ACTION) + "$")
        ],
    },
    fallbacks=[MessageHandler(filters.Regex("^Done$"), stop_command)],
)
