from firstsaturdaybot.commands.user_commands import (
    save_nickname,
    user_start_command,
    set_nickname,
    delete_user_data,
    show_privacy_policy
)
from firstsaturdaybot.commands.common_commads import (
    stop_command,
    incorrect_input
)
from firstsaturdaybot.handlers.ifsconstants import (
    REMOVE_USER,
    SHOW_PRIVACY_POLICY,
    STOP_CONVERSATION,
    SELECTING_USER_ACTION,
    SET_NICKNAME,
    TYPING_NICKNAME
)
from telegram.ext import (
    CommandHandler,
    filters,
    ConversationHandler,
    CallbackQueryHandler,
    MessageHandler
)


user_conversation_handler = ConversationHandler(
    entry_points=[CommandHandler('start', user_start_command, filters=filters.ChatType.PRIVATE)],
    states={
        SELECTING_USER_ACTION: [
            CallbackQueryHandler(
                stop_command,
                pattern="^" + str(STOP_CONVERSATION) + "$")
            ],
        TYPING_NICKNAME: [
            MessageHandler(
                filters.Regex(r"^[a-zA-Z0-9_]{5,}$"),
                save_nickname),
            MessageHandler(
                filters.TEXT & ~filters.COMMAND,
                incorrect_input)
            ],
        SHOW_PRIVACY_POLICY: [
            CallbackQueryHandler(
                stop_command,
                pattern="^" + str(STOP_CONVERSATION) + "$"),
            CallbackQueryHandler(
                delete_user_data,
                pattern="^" + str(REMOVE_USER) + "$")
            ]
    },
    fallbacks=[
        CommandHandler(
            "stop",
            stop_command),
        CallbackQueryHandler(
            user_start_command,
            pattern="^" + str(SELECTING_USER_ACTION) + "$"),
        CallbackQueryHandler(
            set_nickname,
            pattern=f"^{str(SET_NICKNAME)}$"),
        CallbackQueryHandler(
            show_privacy_policy,
            pattern=f"^{str(SHOW_PRIVACY_POLICY)}$"),
        CallbackQueryHandler(
            stop_command,
            pattern=f"^{str(STOP_CONVERSATION)}$"),
        ],
    allow_reentry=True
)
