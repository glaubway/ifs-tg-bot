from firstsaturdaybot.handlers.configuration_model import Config
from firstsaturdaybot.handlers.time_model import EventTime
RUNTIME_CONFIG = Config()
RUNTIME_TIME = EventTime()

from firstsaturdaybot.conversation_handlers.admin_conversation import *
from firstsaturdaybot.conversation_handlers.user_conversation import *
from firstsaturdaybot.conversation_handlers.common_conversation import *
from telegram.ext import (
    ApplicationBuilder
    )

def main():
    application = (ApplicationBuilder()
        .token(RUNTIME_CONFIG.BOT_TOKEN)
        .build())
    application.add_handler(user_conversation_handler)
    application.add_handler(admin_conversation_handler)
    application.add_handler(unknown_handler)

    application.run_polling()