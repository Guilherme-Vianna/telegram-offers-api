import os
from pymongo import MongoClient


class DbClient:
    def get_client(self):
        client = MongoClient(os.getenv("MONGO_URL"))
        db = client.get_database()
        return db['mensagens']
        