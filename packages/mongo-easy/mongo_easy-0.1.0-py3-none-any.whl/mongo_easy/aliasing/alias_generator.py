from ..core import crud
from .registry import register_alias

def generate_aliases(db_instance):
    """
    Automatically creates readable alias functions for collections like:
    - add_user(data) → db.save("users", data)
    - get_orders(filters) → db.find("orders", filters)
    """
    collections = db_instance.list_collections()
    
    for collection in collections:
        name = collection.rstrip("s")  # crude singularization
        register_alias(f"add_{name}", lambda data, c=collection: db_instance.save(c, data))
        register_alias(f"get_{collection}", lambda filters=None, c=collection: db_instance.find(c, filters or {}))
        register_alias(f"delete_{name}", lambda filters, c=collection: db_instance.delete(c, filters))
