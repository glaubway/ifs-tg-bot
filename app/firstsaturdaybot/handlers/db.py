from pymongo import MongoClient, errors
from firstsaturdaybot import RUNTIME_CONFIG
from firstsaturdaybot.handlers.logger import myLogger

logger = myLogger(__name__)

class MongoDB:
    def __init__(self, mongo_url) -> None:
        self.mongo_url = mongo_url
        try:
            self.mongo_client = MongoClient(self.mongo_url)
            self.users_collection = self.mongo_client["ifsbotdb"]["users"]
        except errors.ConnectionFailure as error:
            logger.exception("Could not connect to the server.\n", error)