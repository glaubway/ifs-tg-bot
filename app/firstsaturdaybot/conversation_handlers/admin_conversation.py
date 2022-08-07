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
        TYPING_TIME_CONFIGURATION: [
            CallbackQueryHandler(
                admin_start_command, 
                pattern="^" + str(TO_START) + "$"),
            MessageHandler(
                filters.Regex(r"^[0-2]?[0-9]\:[0-5]?[0-9]$"),
                save_time_configuration
                ),
            MessageHandler(
                filters.TEXT & ~filters.COMMAND,
                incorrect_input
            )
            ],
        TYPING_ADD_ADMIN: [
            CallbackQueryHandler(
                admin_start_command, 
                pattern="^" + str(TO_START) + "$"),
            MessageHandler(
                filters.Regex(r"^[a-zA-Z0-9_]{5,}$"),
                add_admin
                ),
            MessageHandler(
                filters.TEXT & ~filters.COMMAND,
                incorrect_input
            )
            ],
        TYPING_REMOVE_ADMIN: [
            CallbackQueryHandler(
                admin_start_command, 
                pattern="^" + str(TO_START) + "$"),
            CallbackQueryHandler(
                remove_admin, 
                pattern=r"^[a-zA-Z0-9_]{5,}$"),
            MessageHandler(
                filters.TEXT & ~filters.COMMAND,
                incorrect_input
            )
            ],
        TYPING_LINK_CONFIGURATION: [
            CallbackQueryHandler(
                admin_start_command, 
                pattern="^" + str(TO_START) + "$"),
            MessageHandler(
                filters.Regex(r"^https:\/\/.*$"),
                save_link_configuration
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
            set_event_time, 
            pattern=f"^({str(START_EVENT_TIME)}|{str(END_EVENT_TIME)})$"),
        CallbackQueryHandler(
            set_event_admin, 
            pattern=f"^({str(ADD_ADMIN)}|{str(REMOVE_ADMIN)})$"),
        CallbackQueryHandler(
            set_event_link, 
            pattern=f"^({str(SET_FORM_LINK)})$"),
        CallbackQueryHandler(
            show_current_configuration, 
            pattern=f"^{str(SHOW_CURRENT_CONFIGURATION)}$"),
        CallbackQueryHandler(
            stop_nested_command, 
            pattern=f"^{str(STOP_CONVERSATION)}$")
        ],
    allow_reentry=True
)