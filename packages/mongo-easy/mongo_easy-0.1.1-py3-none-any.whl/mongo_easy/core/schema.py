from .connection import get_db

def get_schema(collection, sample_size=10):
    db = get_db()
    docs = db[collection].find().limit(sample_size)
    keys = set()
    for doc in docs:
        keys.update(doc.keys())
    return list(keys)
