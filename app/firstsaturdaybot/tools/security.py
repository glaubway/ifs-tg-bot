
from functools import wraps
from firstsaturdaybot import RUNTIME_CONFIG
from firstsaturdaybot.tools.timemodule import is_firstsaturday
from firstsaturdaybot.tools.logger import myLogger

logger = myLogger(__name__)

def restricted_admin(func):
    @wraps(func)
    async def wrapped(update, context, *args, **kwargs):
        try:
            user_name = update.message.from_user.username
            user_id = update.message.from_user.id
        except AttributeError:
            user_name = update.callback_query.from_user.username
            user_id = update.callback_query.from_user.id
        if not RUNTIME_CONFIG.is_user_admin(user_name):
            logger.warn(f"Unauthorized access denied for {user_name} {user_id}.")
            return
        return await func(update, context, *args, **kwargs)
    return wrapped

def restricted_firstsaturday(func):
    @wraps(func)
    async def wrapped(update, context, *args, **kwargs):
        if not is_firstsaturday():
            return
        return await func(update, context, *args, **kwargs)
    return wrapped
