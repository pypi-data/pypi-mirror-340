alias_registry = {}

def register_alias(name, func):
    alias_registry[name] = func

def get_alias(name):
    return alias_registry.get(name)

def list_aliases():
    return list(alias_registry.keys())
