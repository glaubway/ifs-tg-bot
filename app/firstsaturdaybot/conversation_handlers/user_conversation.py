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
        SELECT_ADMIN_FEATURES: [
            CallbackQueryHandler(select_user_feature, pattern="^" + str(SELECT_ADMIN_FEATURES) + "$")
        ],
    },
    fallbacks=[MessageHandler(filters.Regex("^Done$"), done_command)],
)
