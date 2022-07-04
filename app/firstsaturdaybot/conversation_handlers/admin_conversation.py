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
        SHOW_CURRENT_CONFIGURATION: [
            CallbackQueryHandler(
                admin_start_command, 
                pattern="^" + str(TO_START) + "$")
            ],
        SELECTING_ADMIN_ACTION: [
            CallbackQueryHandler(
                stop_nested_command, 
                pattern="^" + str(STOP_CONVERSATION) + "$")
            ],
        TYPING_CONFIGURATION: [
            CallbackQueryHandler(
                admin_start_command, 
                pattern="^" + str(TO_START) + "$"),
            MessageHandler(
                filters.Regex(r"^[0-2]?[0-9]\:[0-5]?[0-9]$"),
                save_configuration
                ),
            MessageHandler(
                filters.Regex(r"^@[a-zA-Z0-9_]{5,}$"),
                save_configuration
                ),
            MessageHandler(
                filters.Regex(r"^https:\/\/.*$"),
                save_configuration
                ),
            MessageHandler(
                filters.TEXT & ~filters.COMMAND,
                incorrect_input
            )
            ]
    },
    fallbacks=[
        CommandHandler(
            "stop", 
            stop_command),
        CallbackQueryHandler(
            set_event_configuration, 
            pattern=f"^({str(START_EVENT_TIME)}|{str(END_EVENT_TIME)}|{str(ADD_ADMIN)}|{str(REMOVE_ADMIN)}|{str(SET_FORM_LINK)})$"),
        CallbackQueryHandler(
            show_current_configuration, 
            pattern=f"^{str(SHOW_CURRENT_CONFIGURATION)}$"),
        CallbackQueryHandler(
            stop_nested_command, 
            pattern=f"^{str(STOP_CONVERSATION)}$")
        ],
    allow_reentry=True
)
