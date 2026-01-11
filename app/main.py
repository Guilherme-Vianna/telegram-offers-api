import os
from typing import Union
from dotenv import load_dotenv

load_dotenv()

from fastapi import FastAPI

from app.services.DbClient import DbClient

app = FastAPI()
mongo_url = os.getenv("MONGO_URL")

mongo_client = DbClient()

@app.get("/offers")
def read_root(search: Union[str, None] = None):
    client = mongo_client.get_client()
    query = {"mensagem": {"$regex": "http", "$options": "i"}}
    
    if search:
        query = {
            "$and": [
                {"mensagem": {"$regex": "http", "$options": "i"}},
                {"mensagem": {"$regex": search, "$options": "i"}}
            ]
        }

    messages = list(client.find(query, {"_id": 0}))
    return messages
