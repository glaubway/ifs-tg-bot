from firstsaturdaybot.tools.configuration import Config
from firstsaturdaybot.tools.logger import myLogger
RUNTIME_CONFIG = Config()

from firstsaturdaybot.conversation_handlers.admin_conversation import *
from firstsaturdaybot.conversation_handlers.user_conversation import *
from firstsaturdaybot.conversation_handlers.common_conversation import *
from telegram.ext import (
    ApplicationBuilder
    )

def main():
    application = ApplicationBuilder().token(RUNTIME_CONFIG.BOT_TOKEN).build()
    application.add_handler(user_conversation_handler)
    application.add_handler(admin_conversation_handler)
    application.add_handler(unknown_handler)
    application.add_handler(invalid_button_handler)

    application.run_polling()