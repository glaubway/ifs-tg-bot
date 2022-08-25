from typing import List, Dict, Any
from logging import getLogger
from pymongo import MongoClient, errors


logger = getLogger(__name__)


class IFSMongoDatabase:
    mongo_url: str
    mongo_client: MongoClient[Dict[str, Any]]

    def __init__(self, mongo_url: str, city: str) -> None:
        self.mongo_url = mongo_url
        try:
            self.mongo_client = MongoClient(self.mongo_url)
        except errors.ConnectionFailure:
            raise errors.ConnectionFailure("Could not connect to the server.\n")

        self.db_name = self.mongo_client[f'IngressFirstSaturday{city}']
        self.admins_col = self.db_name['admins']
        self.users_col = self.db_name['users']

    def add_admin(self, username: str) -> None:
        if self.admins_col.count_documents({'username': username}) == 0:
            self.admins_col.insert_one({
                'username': username
            })

    def remove_admin(self, username: str) -> bool:
        if self.admins_col.count_documents({'username': username}) == 1:
            self.admins_col.delete_one({
                'username': username
            })
            return True
        return False

    def show_all_admins(self) -> List[str]:
        admins = list(self.admins_col.find())
        return [admin['username'] for admin in admins]
