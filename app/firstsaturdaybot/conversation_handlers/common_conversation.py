from firstsaturdaybot.commands.common_commads import (
    unknown_command,
    stop_nested_command
)
from telegram.ext import (
    MessageHandler,
    filters
)


unknown_handler = MessageHandler((filters.COMMAND & filters.ChatType.PRIVATE), unknown_command)

end_handler = MessageHandler(filters.COMMAND, stop_nested_command)
