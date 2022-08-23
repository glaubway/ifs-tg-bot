from os import environ
from logging import (
    basicConfig,
    getLevelName
)

class IFSConfiguration:
    RUNTIME_ADMINS: list[str]
    BOT_TOKEN: str
    CHAT_ID: str
    GLOBAL_ADMINS: list[str]
    EVENT_CITY: str
    EVENT_DATE_RESTRICTION: bool
    EVENT_TIME_RESTRICTION: bool
    EVENT_LANGUAGE: str
    MONGO_URL: str
    STATISTIC_FORM_LINK: str
    PORTAL_HUNT_SPREADSHEET_LINK: str
    EVENT_TIMEZONE: str
    LOGGING_LEVEL: str

    def __init__(self) -> None:
        self.RUNTIME_ADMINS = []
        self.BOT_TOKEN = self.load_var_from_env('BOT_TOKEN')
        self.CHAT_ID = self.load_var_from_env('CHAT_ID')
        self.GLOBAL_ADMINS = [admin for admin in self.load_var_from_env('GLOBAL_ADMINS').split()]
        self.EVENT_CITY = self.load_var_from_env('EVENT_CITY')
        self.EVENT_DATE_RESTRICTION = self.str2bool(self.load_var_from_env('EVENT_DATE_RESTRICTION'))
        self.EVENT_TIME_RESTRICTION = self.str2bool(self.load_var_from_env('EVENT_TIME_RESTRICTION'))
        self.EVENT_TIMEZONE = self.load_var_from_env('EVENT_TIMEZONE')
        self.EVENT_LANGUAGE = self.load_var_from_env('EVENT_LANGUAGE')
        self.MONGO_URL = self.load_var_from_env('MONGO_URL')
        self.STATISTIC_FORM_LINK = ''
        self.PORTAL_HUNT_SPREADSHEET_LINK = ''
        basicConfig(format='%(asctime)s - %(levelname)s - %(module)s - %(message)s', 
                                      level=getLevelName(self.load_var_from_env('LOGGING_LEVEL')))

    def set_statistic_form_link (self, custom_link: str) -> None:
        self.STATISTIC_FORM_LINK = custom_link

    def set_portal_hunt_spreadsheet_link (self, custom_link: str) -> None:
        self.PORTAL_HUNT_SPREADSHEET_LINK = custom_link

    def change_date_restriction (self) -> None:
        if self.EVENT_DATE_RESTRICTION:
            self.EVENT_DATE_RESTRICTION = False
            self.EVENT_TIME_RESTRICTION = False
        else:
            self.EVENT_DATE_RESTRICTION = True

    def change_time_restriction (self) -> None:
        if self.EVENT_TIME_RESTRICTION:
            self.EVENT_TIME_RESTRICTION = False
        else:
            self.EVENT_TIME_RESTRICTION = True
            self.EVENT_DATE_RESTRICTION = True

    def show_date_restriction (self) -> str:
        if self.EVENT_DATE_RESTRICTION:
            return "Enabled"
        else:
            return "Disabled"

    def show_time_restriction (self) -> str:
        if self.EVENT_TIME_RESTRICTION:
            return "Enabled"
        else:
            return "Disabled"

    def is_user_admin(self, username: str) -> bool:
        if username in self.RUNTIME_ADMINS or username in self.GLOBAL_ADMINS:
            return True
        else:
            return False

    def is_user_predefined_admin(self, username: str) -> bool:
        if username in self.GLOBAL_ADMINS:
            return True
        else:
            return False

    def show_current_admins_as_string(self) -> str:
        if self.RUNTIME_ADMINS:
            return '@' + ' @'.join([*self.GLOBAL_ADMINS, *self.RUNTIME_ADMINS])
        else:
            return '@' + ' @'.join(self.GLOBAL_ADMINS)

    def show_current_admins_as_list(self) -> list[str]:
        if self.RUNTIME_ADMINS:
            return [*self.GLOBAL_ADMINS, *self.RUNTIME_ADMINS]
        else:
            return self.GLOBAL_ADMINS

    def sync_admins_from_db(self, admins: list[str]) -> None:
        if admins:
            self.RUNTIME_ADMINS = admins
        else:
            self.RUNTIME_ADMINS = []

    def str2bool(self, string: str) -> bool:
        if string in ["True", "true"]:
            return True
        else:
            return False

    def load_var_from_env(self, env_name: str) -> str:
        try:
            if environ[env_name] == '':
                raise TypeError(f'Environment variable {env_name} didn\' set correctly.\nPlease check .env file.')
            else:
                return environ[env_name]
        except KeyError:
            raise KeyError(f'Environment variable {env_name} didn\' found.\nPlease check .env file.')
