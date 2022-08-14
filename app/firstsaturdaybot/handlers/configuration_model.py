from asyncio.log import logger
from firstsaturdaybot.handlers.logger import myLogger
from os import environ

logger = myLogger(__name__)

class Config(object):
    
    def __init__(self) -> None:
        self.RUNTIME_ADMINS = []
        self.BOT_TOKEN = self.load_var_from_env('BOT_TOKEN')
        self.CHAT_ID = self.load_var_from_env('CHAT_ID')
        self.GLOBAL_ADMINS = [admin for admin in self.load_var_from_env('GLOBAL_ADMINS').split()]
        self.EVENT_CITY = self.load_var_from_env('EVENT_CITY')
        self.EVENT_DATE_RESTRICTION = self.str2bool(self.load_var_from_env('EVENT_DATE_RESTRICTION'))
        self.EVENT_TIME_RESTRICTION = self.str2bool(self.load_var_from_env('EVENT_TIME_RESTRICTION'))
        self.EVENT_LANGUAGE = self.load_var_from_env('EVENT_LANGUAGE')
        self.MONGO_URL = self.load_var_from_env('MONGO_URL')
        self.STATISTIC_FORM_LINK = ''
        self.PORTAL_HUNT_SPREADSHEET_LINK = ''

    def add_admin(self, username):
        self.RUNTIME_ADMINS.append(username)

    def remove_admin(self, username):
        self.RUNTIME_ADMINS.remove(username)
        return True

    def set_statistic_form_link (self, custom_link):
        self.STATISTIC_FORM_LINK = custom_link

    def set_portal_hunt_spreadsheet_link (self, custom_link):
        self.PORTAL_HUNT_SPREADSHEET_LINK = custom_link

    def change_date_restriction (self):
        if self.EVENT_DATE_RESTRICTION:
            self.EVENT_DATE_RESTRICTION = False
            self.EVENT_TIME_RESTRICTION = False
        else:
            self.EVENT_DATE_RESTRICTION = True

    def change_time_restriction (self):
        if self.EVENT_TIME_RESTRICTION:
            self.EVENT_TIME_RESTRICTION = False
        else:
            self.EVENT_TIME_RESTRICTION = True
            self.EVENT_DATE_RESTRICTION = True

    def show_date_restriction (self):
        if self.EVENT_DATE_RESTRICTION:
            return "Enabled"
        else:
            return "Disabled"

    def show_time_restriction (self):
        if self.EVENT_TIME_RESTRICTION:
            return "Enabled"
        else:
            return "Disabled"

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
                logger.exception(f'Environment variable {env_name} didn\'t set correctly.\nPlease check .env file.')
                raise TypeError
            else:
                return environ[env_name]
        except KeyError as error:
            logger.exception(f'Environment variable {env_name} didn\'t found.\nPlease check .env file.')
            raise error

    def str2bool(self, string):
        if string in ["True", "true"]:
            return True
        else:
            return False