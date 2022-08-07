from asyncio.log import logger
from cmath import log
from firstsaturdaybot.tools.logger import myLogger
from os import environ

logger = myLogger(__name__)

class Config(object):
    
    def __init__(self) -> None:
        self.RUNTIME_ADMINS = []
        self.EVENT_START_TIME = '00:00'
        self.EVENT_END_TIME = '01:00'
        self.BOT_TOKEN = self.load_var_from_env('BOT_TOKEN')
        self.CHAT_ID = self.load_var_from_env('CHAT_ID')
        self.GLOBAL_ADMINS = [admin for admin in self.load_var_from_env('GLOBAL_ADMINS').split()]
        self.EVENT_CITY = self.load_var_from_env('EVENT_CITY')
        self.EVENT_TIMEZONE = self.load_var_from_env('EVENT_TIMEZONE')
        self.EVENT_LANGUAGE = self.load_var_from_env('EVENT_LANGUAGE')
        self.MONGO_URL = self.load_var_from_env('MONGO_URL')
        self.FORM_LINK = ''

    def add_admin(self, username):
        self.RUNTIME_ADMINS.append(username)

    def remove_admin(self, username):
        self.RUNTIME_ADMINS.remove(username)
        return True

    def set_start_time (self, time):
        self.EVENT_START_TIME = time
        
    def set_end_time (self, time):
        self.EVENT_END_TIME = time

    def set_form_link (self, form_link):
        self.FORM_LINK = form_link

    def is_user_admin(self, username):
        if username in self.RUNTIME_ADMINS or username in self.GLOBAL_ADMINS:
            return True

    def is_user_predefined_admin(self, username):
        if username in self.GLOBAL_ADMINS:
            return True

    def show_current_admins_as_string(self):
        if self.RUNTIME_ADMINS:
            return ' '.join([*self.GLOBAL_ADMINS, *self.RUNTIME_ADMINS])
        else:
            return ' '.join(self.GLOBAL_ADMINS)

    def show_current_admins_as_list(self):
        if self.RUNTIME_ADMINS:
            return [*self.GLOBAL_ADMINS, *self.RUNTIME_ADMINS]
        else:
            return self.GLOBAL_ADMINS

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
           