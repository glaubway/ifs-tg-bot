from logging import getLogger
from calendar import monthcalendar
from datetime import datetime, tzinfo
import pytz

logger = getLogger(__name__)

class IFSEventTime:
    EVENT_START_TIME: dict[int]
    EVENT_END_TIME: dict[int]
    EVENT_TIMEZONE: tzinfo
    
    def __init__(self, timezone: str) -> None:
        self.EVENT_START_TIME = {"hour": 0, "minute": 00}
        self.EVENT_END_TIME = {"hour": 1, "minute": 00}
        if pytz.timezone(timezone):
            self.EVENT_TIMEZONE = pytz.timezone(timezone)
        else: 
            logger.info('Incorect timezone. Using UTC.')
            self.EVENT_TIMEZONE = pytz.timezone('UTC')

    def right_now(self) -> datetime:
        return datetime.now(self.EVENT_TIMEZONE)
    
    def first_saturday_of_month(self) -> int:
        year = self.right_now().year
        month = self.right_now().month
        if monthcalendar(year, month)[0][5] == 0:
            return monthcalendar(year, month)[1][5]
        else:
            return monthcalendar(year, month)[0][5]

    def is_firstsaturday_today(self) -> bool:
        if self.first_saturday_of_month() == self.right_now().day:
            return True
        else:
            return False

    def is_event_time(self) -> bool:
        if self.event_is_started() and not self.event_is_ended():
            return True
        else:
            return False

    def event_is_started(self) -> bool:
        if self.right_now() >= self.start_time():
            return True
        else:
            return False 

    def event_is_ended(self) -> bool:
        if self.right_now() >= self.end_time():
            return True
        else:
            return False 

    def start_time(self) -> datetime:
        return self.right_now().replace(hour=self.EVENT_START_TIME["hour"], 
                                            minute=self.EVENT_START_TIME["minute"], 
                                            second=0, 
                                            microsecond=0)

    def end_time(self) -> datetime:
        return self.right_now().replace(hour=self.EVENT_END_TIME["hour"], 
                                            minute=self.EVENT_END_TIME["minute"], 
                                            second=0, 
                                            microsecond=0)

    def check_time(self, new_hour: int, new_minute: int) -> datetime:
        return self.right_now().replace(hour=new_hour, 
                                            minute=new_minute, 
                                            second=0, 
                                            microsecond=0)

    def set_start_time (self, time: str) -> bool:
        new_hour = int(time.split(":")[0])
        new_minute = int(time.split(":")[1])
        if self.end_time() > self.check_time(new_hour, new_minute):
            self.EVENT_START_TIME = {"hour": new_hour, "minute": new_minute}
            return True
        else:
            return False
        
    def set_end_time (self, time: str) -> bool:
        new_hour = int(time.split(":")[0])
        new_minute = int(time.split(":")[1])
        if self.start_time() < self.check_time(new_hour, new_minute):
            self.EVENT_END_TIME = {"hour": new_hour, "minute": new_minute}
            return True
        else:
            return False
