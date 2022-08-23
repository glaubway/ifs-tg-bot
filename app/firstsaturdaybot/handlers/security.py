from functools import wraps
from logging import getLogger
from firstsaturdaybot import IFSCONFIGURATION, IFSEVENTTIME
from firstsaturdaybot.commands.common_commads import reply_message

from telegram import (
    Update
    )
from telegram.ext import (
    ContextTypes
    )

logger = getLogger(__name__)

def restricted_admin(func):
    @wraps(func)
    async def wrapped(update: Update, context: ContextTypes.DEFAULT_TYPE, *args, **kwargs):
        user_name: str
        conv_type: str
        user_id: int
        text: str
        try:
            user_name = update.message.from_user.username
            user_id = update.message.from_user.id
            conv_type = "message"
        except AttributeError:
            user_name = update.callback_query.from_user.username
            user_id = update.callback_query.from_user.id
            conv_type = "callback"
        text = "Unauthorized access denied"
        if not IFSCONFIGURATION.is_user_admin(user_name):
            logger.warn(f"Unauthorized access denied for {user_name} {user_id}.")
            await reply_message(conv_type, text, update, context)
            return
        return await func(update, context, *args, **kwargs)
    return wrapped

def restricted_firstsaturday(func):
    @wraps(func)
    async def wrapped(update: Update, context: ContextTypes.DEFAULT_TYPE, *args, **kwargs):
        user_name: str
        conv_type: str
        text: str
        try:
            user_name = update.message.from_user.username
            conv_type = "message"
        except AttributeError:
            user_name = update.callback_query.from_user.username
            conv_type = "callback"
        text = f"Hi {user_name}!\n"
        text += "Event hasn't been started yet or already ended, please retun to me at the first saturday of month."
        if IFSCONFIGURATION.EVENT_DATE_RESTRICTION and not IFSEVENTTIME.is_firstsaturday_today():
            if IFSCONFIGURATION.EVENT_TIME_RESTRICTION and not IFSEVENTTIME.is_event_time():
                await reply_message(conv_type, text, update, context)
                return
            elif IFSCONFIGURATION.EVENT_TIME_RESTRICTION and IFSEVENTTIME.is_event_time():
                return await func(update, context, *args, **kwargs)
            else:
                await reply_message(conv_type, text, update, context)
                return 
        return await func(update, context, *args, **kwargs)
    return wrapped
