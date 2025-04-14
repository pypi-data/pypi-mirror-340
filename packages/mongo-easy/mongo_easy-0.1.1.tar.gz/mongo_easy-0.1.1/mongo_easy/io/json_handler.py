import json
from ..core.connection import get_db

def import_json(collection, filepath):
    db = get_db()
    with open(filepath, 'r', encoding='utf-8') as f:
        data = json.load(f)
        if isinstance(data, dict):
            db[collection].insert_one(data)
        else:
            db[collection].insert_many(data)
    print(f"✔ Imported JSON into '{collection}'")

def export_json(collection, filepath):
    db = get_db()
    docs = list(db[collection].find())
    for doc in docs:
        doc["_id"] = str(doc["_id"])  # Serialize ObjectId
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(docs, f, indent=2)
    print(f"✔ Exported '{collection}' to JSON: {filepath}")
