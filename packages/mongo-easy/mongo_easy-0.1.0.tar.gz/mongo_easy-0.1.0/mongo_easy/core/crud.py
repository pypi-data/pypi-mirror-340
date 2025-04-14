from .connection import get_db

def save(collection, data):
    db = get_db()
    return db[collection].insert_one(data)

def save_many(collection, data_list):
    db = get_db()
    return db[collection].insert_many(data_list)

def find(collection, filters=None):
    db = get_db()
    return list(db[collection].find(filters or {}))

def find_one(collection, filters=None):
    db = get_db()
    return db[collection].find_one(filters or {})

def update(collection, filters, updates):
    db = get_db()
    return db[collection].update_many(filters, {"$set": updates})

def delete(collection, filters):
    db = get_db()
    return db[collection].delete_many(filters)

def delete_all(collection):
    db = get_db()
    return db[collection].delete_many({})
