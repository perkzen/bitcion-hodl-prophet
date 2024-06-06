from pymongo import MongoClient

from src.config import settings

_client = MongoClient(settings.database_url)

db = _client[settings.database_name]
