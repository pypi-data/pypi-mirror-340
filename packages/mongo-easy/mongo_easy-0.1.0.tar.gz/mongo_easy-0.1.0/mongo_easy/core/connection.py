from pymongo import MongoClient

_client = None
_db = None

def connect(uri="mongodb://localhost:27017", db_name="test"):
    global _client, _db
    _client = MongoClient(uri)
    _db = _client[db_name]
    print(f"✔ Connected to MongoDB database: '{db_name}'")

def get_db():
    if _db is None:
        connect()  # use defaults
    return _db

def use_database(db_name):
    global _db
    if _client is None:
        connect()
    _db = _client[db_name]
