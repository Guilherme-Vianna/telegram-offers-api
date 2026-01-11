import os
import re
from typing import Union
from dotenv import load_dotenv

load_dotenv()

from fastapi import FastAPI

from app.services.DbClient import DbClient

app = FastAPI()
mongo_url = os.getenv("MONGO_URL")

mongo_client = DbClient()

@app.get("/offers")
def read_root(search: Union[str, None] = None, limit: int = 100):
    client = mongo_client.get_client()
    query = {"mensagem": {"$regex": "http", "$options": "i"}}
    
    if search:
        query = {
            "$and": [
                {"mensagem": {"$regex": "http", "$options": "i"}},
                {"mensagem": {"$regex": search, "$options": "i"}}
            ]
        }

    # Sort by _id descending (newest first) and apply limit
    cursor = client.find(query, {"_id": 0}).sort("_id", -1).limit(limit)
    results = []
    
    for doc in cursor:
        message = doc.get("mensagem", "")
        # Find the first link in the message
        url_match = re.search(r'(https?://\S+)', message)
        link = url_match.group(0) if url_match else None
        
        results.append({
            "message": message,
            "link": link
        })

    return results
