from firstsaturdaybot.handlers.ifsconfiguration import IFSConfiguration
from firstsaturdaybot.handlers.ifseventtime import IFSEventTime
from firstsaturdaybot.handlers.ifsmongodatabases import IFSMongoDatabase
RUNTIME_CONFIG = IFSConfiguration()
RUNTIME_TIME = IFSEventTime()
RUNTIME_DATABASE = IFSMongoDatabase(RUNTIME_CONFIG.MONGO_URL, RUNTIME_CONFIG.EVENT_CITY)
RUNTIME_CONFIG.sync_admins_from_db(RUNTIME_DATABASE.show_all_admins())

from firstsaturdaybot.conversation_handlers.admin_conversation import *
from firstsaturdaybot.conversation_handlers.user_conversation import *
from firstsaturdaybot.conversation_handlers.common_conversation import *
from telegram.ext import (
    ApplicationBuilder
    )

def main() -> None:
    application = (ApplicationBuilder()
        .token(RUNTIME_CONFIG.BOT_TOKEN)
        .build())
    application.add_handler(user_conversation_handler)
    application.add_handler(admin_conversation_handler)
    application.add_handler(unknown_handler)

    application.run_polling()