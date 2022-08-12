from calendar import monthcalendar
from datetime import datetime
from os import environ
import pytz
from firstsaturdaybot.tools.logger import myLogger

logger = myLogger(__name__)

class EventTime():
    def __init__(self) -> None:
        self.EVENT_START_TIME = {"hour": 0, "minute": 00}
        self.EVENT_END_TIME = {"hour": 1, "minute": 00}
        if pytz.timezone(self.load_var_from_env('EVENT_TIMEZONE')):
            self.EVENT_TIMEZONE = pytz.timezone(self.load_var_from_env('EVENT_TIMEZONE'))
        else: 
            logger.exception('Incorect timezone. Using UTC.')
            self.EVENT_TIMEZONE = pytz.timezone('UTC')

    def right_now(self):
        return datetime.now(self.EVENT_TIMEZONE)
    
    def first_saturday_of_month(self):
        year = self.right_now().year
        month = self.right_now().month
        if monthcalendar(year, month)[0][5] == 0:
            return monthcalendar(year, month)[1][5]
        else:
            return monthcalendar(year, month)[0][5]

    def is_firstsaturday_today(self):
        if self.first_saturday_of_month() == self.right_now().day:
            return True
        else:
            return False

    def is_event_time(self):
        if self.event_is_started() and not self.event_is_ended():
            return True
        else:
            return False

    def event_is_started(self):
        if self.right_now() >= self.start_time():
            return True
        else:
            return False 

    def event_is_ended(self):
        if self.right_now() >= self.end_time():
            return True
        else:
            return False 

    def start_time(self):
        return self.right_now().replace(hour=self.EVENT_START_TIME["hour"], 
                                            minute=self.EVENT_START_TIME["minute"], 
                                            second=0, 
                                            microsecond=0)

    def end_time(self):
        return self.right_now().replace(hour=self.EVENT_END_TIME["hour"], 
                                            minute=self.EVENT_END_TIME["minute"], 
                                            second=0, 
                                            microsecond=0)

    def check_time(self, new_hour, new_minute):
        return self.right_now().replace(hour=new_hour, 
                                            minute=new_minute, 
                                            second=0, 
                                            microsecond=0)

    def set_start_time (self, time):
        new_hour = int(time.split(":")[0])
        new_minute = int(time.split(":")[1])
        if self.end_time() > self.check_time(new_hour, new_minute):
            self.EVENT_START_TIME = {"hour": new_hour, "minute": new_minute}
            return True
        else:
            return False
        
    def set_end_time (self, time):
        new_hour = int(time.split(":")[0])
        new_minute = int(time.split(":")[1])
        if self.start_time() < self.check_time(new_hour, new_minute):
            self.EVENT_END_TIME = {"hour": new_hour, "minute": new_minute}
            return True
        else:
            return False
        

    def load_var_from_env(self, env_name):
        try:
            if environ[env_name] == '':
                logger.exception(f'Environment variable {env_name} didn\' set correctly.\nPlease check .env file.')
                raise TypeError
            else:
                return environ[env_name]
        except KeyError as error:
            logger.exception(f'Environment variable {env_name} didn\' found.\nPlease check .env file.')
            raise error
