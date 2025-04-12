# config/utils.py

import os

def get_bool_env(key, default=False):
    """
    Retrieve a boolean environment variable.
    Accepts: '1', 'true', 'yes' (case-insensitive) as True.
    Everything else is False.
    """
    val = os.getenv(key)
    if val is None:
        return default
    return val.strip().lower() in ('1', 'true', 'yes')
