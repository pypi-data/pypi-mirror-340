import argparse
from ..core.connection import get_db
from ..core.crud import find, save, delete
from ..io.csv_handler import import_csv, export_csv

def main():
    parser = argparse.ArgumentParser(prog="mongo-easy", description="Simple CLI for MongoDB")

    subparsers = parser.add_subparsers(dest="command")

    # list collections
    subparsers.add_parser("list", help="List all collections")

    # find
    find_parser = subparsers.add_parser("find", help="Find documents")
    find_parser.add_argument("collection")
    find_parser.add_argument("--filter", default="{}", help='JSON string of filter (e.g. \'{"name": "Alice"}\')')

    # insert
    insert_parser = subparsers.add_parser("insert", help="Insert a document")
    insert_parser.add_argument("collection")
    insert_parser.add_argument("--data", required=True, help='JSON string of document (e.g. \'{"name": "Bob"}\')')

    # delete
    delete_parser = subparsers.add_parser("delete", help="Delete documents")
    delete_parser.add_argument("collection")
    delete_parser.add_argument("--filter", required=True, help="JSON string filter")

    # csv import/export
    import_parser = subparsers.add_parser("import-csv", help="Import CSV to a collection")
    import_parser.add_argument("collection")
    import_parser.add_argument("filepath")

    export_parser = subparsers.add_parser("export-csv", help="Export collection to CSV")
    export_parser.add_argument("collection")
    export_parser.add_argument("filepath")

    args = parser.parse_args()
    db = get_db()  # Uses default or config

    # Command Handlers
    if args.command == "list":
        print("\n".join(db.list_collections()))

    elif args.command == "find":
        import json
        query = json.loads(args.filter)
        results = find(db, args.collection, query)
        for doc in results:
            print(doc)

    elif args.command == "insert":
        import json
        doc = json.loads(args.data)
        save(db, args.collection, doc)
        print("✔ Document inserted.")

    elif args.command == "delete":
        import json
        query = json.loads(args.filter)
        delete(db, args.collection, query)
        print("✔ Documents deleted.")

    elif args.command == "import-csv":
        import_csv(db, args.collection, args.filepath)

    elif args.command == "export-csv":
        export_csv(db, args.collection, args.filepath)

    else:
        parser.print_help()


if __name__ == "__main__":
    main()
