from firstsaturdaybot.commands.common_commads import (
    unknown_command,
    stop_command,
    invalid_button_command
)
from telegram.ext import (
    CallbackQueryHandler,
    MessageHandler,
    filters
)


unknown_command_handler = MessageHandler((filters.COMMAND & filters.ChatType.PRIVATE), unknown_command)

end_handler = MessageHandler(filters.COMMAND, stop_command)

unknown_keyboard_handler = CallbackQueryHandler(invalid_button_command)
