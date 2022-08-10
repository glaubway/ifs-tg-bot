from firstsaturdaybot.commands.common_commads import *
from firstsaturdaybot.commands import *


from telegram.ext import (
    MessageHandler, 
    filters, 
    CallbackQueryHandler)

unknown_handler = MessageHandler((filters.COMMAND & filters.ChatType.PRIVATE), unknown_command)

end_handler = MessageHandler(filters.COMMAND, end_command)