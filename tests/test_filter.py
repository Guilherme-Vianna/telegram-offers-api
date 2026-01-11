from unittest.mock import MagicMock, patch
import os
import sys

sys.path.append(os.getcwd())

from app.main import read_root, mongo_client

def test_read_root_search():
    # Setup mock
    mock_db_collection = MagicMock()
    original_get_client = mongo_client.get_client
    
    try:
        mongo_client.get_client = MagicMock(return_value=mock_db_collection)
        mock_cursor = MagicMock()
        mock_db_collection.find.return_value = mock_cursor
        mock_cursor.__iter__.return_value = []
        
        # Test 1: No search param
        read_root(search=None)
        args, _ = mock_db_collection.find.call_args
        query = args[0]
        assert query == {"mensagem": {"$regex": "http", "$options": "i"}}
        print("Test 1 Passed: Default query correct.")
        
        # Test 2: With search param
        read_root(search="iphone")
        args, _ = mock_db_collection.find.call_args
        query = args[0]
        assert "$and" in query
        assert len(query["$and"]) == 2
        assert query["$and"][0] == {"mensagem": {"$regex": "http", "$options": "i"}}
        assert query["$and"][1] == {"mensagem": {"$regex": "iphone", "$options": "i"}}
        print("Test 2 Passed: Search query correct.")
        
    finally:
        mongo_client.get_client = original_get_client

if __name__ == "__main__":
    test_read_root_search()
