from calendar import monthcalendar
from datetime import datetime
import pytz
from firstsaturdaybot import RUNTIME_CONFIG
from firstsaturdaybot.tools.logger import myLogger

logger = myLogger(__name__)

try:
    local_tz = pytz.timezone(RUNTIME_CONFIG.EVENT_TIMEZONE)
except pytz.exceptions.UnknownTimeZoneError:
    logger.exception('Incorect timezone. Using UTC.')
    RUNTIME_CONFIG.EVENT_TIMEZONE = 'UTC'
    local_tz = pytz.timezone('UTC')

def is_firstsaturday():
    today = datetime.now(local_tz)
    if firstsaturday(today.year, today.month) == today.day:
        return True
    else:
        return False

def firstsaturday(year, month):
    if monthcalendar(year,month)[0][5] == 0:
        return monthcalendar(year,month)[1][5]
    else:
        return monthcalendar(year,month)[0][5]

def current_date():
    today = datetime.now(local_tz)
    return [today.year, today.month]