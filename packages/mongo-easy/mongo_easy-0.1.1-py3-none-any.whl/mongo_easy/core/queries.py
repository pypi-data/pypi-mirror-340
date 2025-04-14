from .connection import get_db

def find_sorted(collection, filters=None, sort_by="_id", direction=1):
    db = get_db()
    return list(db[collection].find(filters or {}).sort(sort_by, direction))

def find_recent(collection, limit=10):
    db = get_db()
    return list(db[collection].find().sort("_id", -1).limit(limit))

def count(collection, filters=None):
    db = get_db()
    return db[collection].count_documents(filters or {})

def exists(collection, filters):
    db = get_db()
    return db[collection].count_documents(filters) > 0

def distinct_values(collection, field):
    db = get_db()
    return db[collection].distinct(field)
