from firstsaturdaybot.handlers.ifsconfiguration import IFSConfiguration
IFSCONFIGURATION = IFSConfiguration()
from firstsaturdaybot.handlers.ifseventtime import IFSEventTime
IFSEVENTTIME = IFSEventTime(IFSCONFIGURATION.EVENT_TIMEZONE)
from firstsaturdaybot.handlers.ifsmongodatabases import IFSMongoDatabase
IFSDATABASE = IFSMongoDatabase(IFSCONFIGURATION.MONGO_URL, IFSCONFIGURATION.EVENT_CITY)

from firstsaturdaybot.conversation_handlers.admin_conversation import (
    admin_conversation_handler
)
from firstsaturdaybot.conversation_handlers.user_conversation import (
    user_conversation_handler
)
from firstsaturdaybot.conversation_handlers.common_conversation import (
    unknown_command_handler,
    unknown_keyboard_handler
)
from telegram.ext import (
    ApplicationBuilder
)


def main() -> None:
    IFSCONFIGURATION.sync_admins_from_db(IFSDATABASE.show_all_admins())
    application = (ApplicationBuilder()
                   .token(IFSCONFIGURATION.BOT_TOKEN)
                   .build())
    application.add_handler(user_conversation_handler)
    application.add_handler(admin_conversation_handler)
    application.add_handler(unknown_command_handler)
    application.add_handler(unknown_keyboard_handler)

    application.run_polling()
