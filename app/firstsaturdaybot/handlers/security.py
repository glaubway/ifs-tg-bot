from firstsaturdaybot import IFSCONFIGURATION, IFSEVENTTIME
from firstsaturdaybot.commands.common_commads import reply_message
from functools import wraps
from logging import getLogger
from telegram import Update
from telegram.ext import ContextTypes
from typing import Any, Callable, TypeVar, cast
T = TypeVar('T', bound=Callable[..., Any])

logger = getLogger(__name__)


def restricted_admin(func: T) -> T:
    @wraps(func)
    async def wrapped(update: Update, context: ContextTypes.DEFAULT_TYPE, *args: Any, **kwargs: Any) -> Any:
        user_name: str = update.effective_user.username
        user_id: int = update.effective_user.id
        text: str = "Unauthorized access denied"
        if not IFSCONFIGURATION.is_user_admin(user_name):
            logger.warn(f"Unauthorized access denied for {user_name} {user_id}.")
            return await reply_message(text, update, context)
        return await func(update, context, *args, **kwargs)
    return cast(T, wrapped)


def restricted_firstsaturday(func: T) -> T:
    @wraps(func)
    async def wrapped(update: Update, context: ContextTypes.DEFAULT_TYPE, *args: Any, **kwargs: Any) -> Any:
        user_name: str = update.effective_user.username
        text: str = f"Hi {user_name}!\n"
        text += "Event hasn't been started yet or already ended, please retun to me at the first saturday of month."
        if IFSCONFIGURATION.EVENT_DATE_RESTRICTION and not IFSEVENTTIME.is_firstsaturday_today():
            return await reply_message(text, update, context)
        if IFSCONFIGURATION.EVENT_TIME_RESTRICTION and not IFSEVENTTIME.is_event_time():
            return await reply_message(text, update, context)
        else:
            return await func(update, context, *args, **kwargs)
    return cast(T, wrapped)
