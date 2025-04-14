import csv
from ..core.connection import get_db

def import_csv(collection, filepath):
    db = get_db()
    with open(filepath, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        db[collection].insert_many(list(reader))
    print(f"✔ Imported CSV into '{collection}'")

def export_csv(collection, filepath):
    db = get_db()
    docs = db[collection].find()
    docs = list(docs)

    if not docs:
        print("⚠ No documents to export.")
        return

    with open(filepath, mode='w', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=docs[0].keys())
        writer.writeheader()
        writer.writerows(docs)
    print(f"✔ Exported '{collection}' to CSV: {filepath}")
