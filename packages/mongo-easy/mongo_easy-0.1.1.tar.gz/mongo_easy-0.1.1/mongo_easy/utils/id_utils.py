from bson import ObjectId
from bson.errors import InvalidId

def is_valid_objectid(id_str):
    try:
        ObjectId(id_str)
        return True
    except (InvalidId, TypeError):
        return False

def str_to_objectid(id_str):
    if is_valid_objectid(id_str):
        return ObjectId(id_str)
    raise ValueError(f"Invalid ObjectId: {id_str}")
