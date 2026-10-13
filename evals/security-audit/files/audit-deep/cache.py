import os
import pickle

CACHE_DIR = os.environ.get("CACHE_DIR", "/var/cache/shop")


def load_cached(key):
    with open(os.path.join(CACHE_DIR, key + ".pkl"), "rb") as f:
        return pickle.loads(f.read())
