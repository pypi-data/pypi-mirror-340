import json
from ..core.connection import get_db

def backup_database(filepath):
    db = get_db()
    dump = {}
    for name in db.list_collection_names():
        docs = list(db[name].find())
        for doc in docs:
            doc["_id"] = str(doc["_id"])
        dump[name] = docs
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(dump, f, indent=2)
    print(f"✔ Full database backed up to {filepath}")

def restore_database(filepath):
    db = get_db()
    with open(filepath, 'r', encoding='utf-8') as f:
        dump = json.load(f)
        for name, docs in dump.items():
            db[name].insert_many(docs)
    print(f"✔ Database restored from {filepath}")
