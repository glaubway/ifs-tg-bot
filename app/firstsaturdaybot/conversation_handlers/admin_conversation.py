from firstsaturdaybot.commands.admin_commands import (
    admin_start_command,
    save_time_configuration,
    incorrect_input,
    add_admin,
    remove_admin,
    save_link_configuration,
    set_event_admin,
    set_event_restriction_policy,
    set_event_link,
    set_event_time,
    change_date_restriction,
    change_time_restriction,
    show_current_configuration
)
from firstsaturdaybot.commands.common_commads import (
    stop_command,
    stop_nested_command
)
from firstsaturdaybot.commands import (
    STOP_CONVERSATION,
    TO_START,
    SELECTING_ADMIN_ACTION,
    SET_START_EVENT_TIME,
    SET_END_EVENT_TIME,
    ADD_ADMIN,
    REMOVE_ADMIN,
    SET_STATISTIC_FORM_LINK,
    SET_PORTAL_HUNT_SPREADSHEET_LINK,
    SET_EVENT_RESTRICTION_POLICY,
    CHANGE_DATE_RESTRICTION,
    CHANGE_TIME_RESTRICTION,
    TYPING_TIME_CONFIGURATION,
    TYPING_STATISTIC_SPREADSHEET_LINK,
    TYPING_PORTAL_HUNT_SPREADSHEET_LINK,
    TYPING_ADD_ADMIN,
    TYPING_REMOVE_ADMIN,
    TYPING_EVENT_RESTRICTION,
    SHOW_CURRENT_CONFIGURATION
)
from telegram.ext import (
    CommandHandler,
    MessageHandler,
    filters,
    ConversationHandler,
    CallbackQueryHandler
)


admin_conversation_handler = ConversationHandler(
    entry_points=[
        CommandHandler(
            'configure',
            admin_start_command,
            filters=filters.ChatType.PRIVATE)
            ],
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
                filters.Regex(r"^(([0-1]?[0-9])|([2][0-3]))\:[0-5]?[0-9]$"),
                save_time_configuration),
            MessageHandler(
                filters.TEXT & ~filters.COMMAND,
                incorrect_input)
            ],
        TYPING_ADD_ADMIN: [
            CallbackQueryHandler(
                admin_start_command,
                pattern="^" + str(TO_START) + "$"),
            MessageHandler(
                filters.Regex(r"^[a-zA-Z0-9_]{5,}$"),
                add_admin),
            MessageHandler(
                filters.TEXT & ~filters.COMMAND,
                incorrect_input)
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
                incorrect_input)
            ],
        TYPING_STATISTIC_SPREADSHEET_LINK: [
            CallbackQueryHandler(
                admin_start_command,
                pattern="^" + str(TO_START) + "$"),
            MessageHandler(
                filters.Regex(r"^https:\/\/.*$"),
                save_link_configuration),
            MessageHandler(
                filters.TEXT & ~filters.COMMAND,
                incorrect_input)
            ],
        TYPING_PORTAL_HUNT_SPREADSHEET_LINK: [
            CallbackQueryHandler(
                admin_start_command,
                pattern="^" + str(TO_START) + "$"),
            MessageHandler(
                filters.Regex(r"^https:\/\/.*$"),
                save_link_configuration),
            MessageHandler(
                filters.TEXT & ~filters.COMMAND,
                incorrect_input)
            ],
        TYPING_EVENT_RESTRICTION: [
            CallbackQueryHandler(
                admin_start_command,
                pattern="^" + str(TO_START) + "$"),
            CallbackQueryHandler(
                change_date_restriction,
                pattern="^" + str(CHANGE_DATE_RESTRICTION) + "$"),
            CallbackQueryHandler(
                change_time_restriction,
                pattern="^" + str(CHANGE_TIME_RESTRICTION) + "$"),
            MessageHandler(
                filters.TEXT & ~filters.COMMAND,
                incorrect_input)
            ]
    },
    fallbacks=[
        CommandHandler(
            "stop",
            stop_command),
        CallbackQueryHandler(
            set_event_time,
            pattern=f"^({str(SET_START_EVENT_TIME)}|{str(SET_END_EVENT_TIME)})$"),
        CallbackQueryHandler(
            set_event_admin,
            pattern=f"^({str(ADD_ADMIN)}|{str(REMOVE_ADMIN)})$"),
        CallbackQueryHandler(
            set_event_link,
            pattern=f"^({str(SET_STATISTIC_FORM_LINK)}|{str(SET_PORTAL_HUNT_SPREADSHEET_LINK)})$"),
        CallbackQueryHandler(
            set_event_restriction_policy,
            pattern=f"^({str(SET_EVENT_RESTRICTION_POLICY)})$"),
        CallbackQueryHandler(
            show_current_configuration,
            pattern=f"^{str(SHOW_CURRENT_CONFIGURATION)}$"),
        CallbackQueryHandler(
            stop_nested_command,
            pattern=f"^{str(STOP_CONVERSATION)}$")
        ],
    allow_reentry=True
)
