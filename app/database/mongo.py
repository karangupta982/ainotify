"""
MongoDB connection helper for user auth/profile/channel storage.
This does not affect the existing Postgres-backed pipeline.
"""

import os
from functools import lru_cache
from pymongo import MongoClient


@lru_cache(maxsize=1)
def get_mongo_client() -> MongoClient:
    mongo_url = os.getenv("MONGODB_URL")
    if not mongo_url:
        raise RuntimeError("MONGODB_URL is not configured")
    return MongoClient(mongo_url, serverSelectionTimeoutMS=5000)


def get_db():
    client = get_mongo_client()
    db_name = os.getenv("MONGODB_DB", "ainotify")
    return client[db_name]


