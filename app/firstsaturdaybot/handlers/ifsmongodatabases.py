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

    def load_user_information(self, id: int) -> Dict[str, str]:
        user = self.users_col.find_one({'_id': id},
                                       {'_id': 0,
                                        'nickname': 1,
                                        'language': 1})
        return user

    def register_user(self, id: int, nickname: str) -> bool:
        try:
            self.users_col.insert_one({
                '_id': id,
                'nickname': nickname,
                'language': 'en'
            })
            return True
        except errors:
            return False

    def find_user(self, id: int) -> bool:
        if self.users_col.count_documents({'_id': id}):
            return True
        return False

    def update_user(self, id: int, values_to_update: Dict[str, str]) -> bool:
        try:
            self.users_col.update_one(
                {'_id': id},
                {'$set': values_to_update}
            )
            return True
        except errors:
            return False

    def delete_user(self, id: int) -> bool:
        try:
            self.users_col.delete_one(
                {'_id': id}
            )
            return True
        except errors:
            return False
