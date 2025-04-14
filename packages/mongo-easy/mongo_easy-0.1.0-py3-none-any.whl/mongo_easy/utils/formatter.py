import re

def snake_case(text):
    text = re.sub(r'[\s\-]+', '_', text)
    return re.sub(r'([A-Z])', r'_\1', text).lower().strip('_')

def clean_keys(data: dict) -> dict:
    """Cleans keys of a dict to make them Mongo-safe (no dots or $)"""
    cleaned = {}
    for k, v in data.items():
        safe_key = k.replace('.', '_').replace('$', '_')
        cleaned[safe_key] = v
    return cleaned
