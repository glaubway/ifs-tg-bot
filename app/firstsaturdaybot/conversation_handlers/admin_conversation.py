from firstsaturdaybot.commands.admin_commands import *
from firstsaturdaybot.commands.common_commads import *
from firstsaturdaybot.commands import *

from telegram.ext import (
    CommandHandler, 
    MessageHandler, 
    filters, 
    ConversationHandler, 
    CallbackQueryHandler)

admin_conversation_handler = ConversationHandler(
    entry_points=[CommandHandler('configure', admin_start_command)],
    states={
        STOPPING: [
            CommandHandler("configure", admin_start_command)
        ],
    },
    fallbacks=[CommandHandler("stop", stop_command)],
)
