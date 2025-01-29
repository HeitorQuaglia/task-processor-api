from motor.motor_asyncio import AsyncIOMotorClient
import os


class MongoDB:
    _client: AsyncIOMotorClient = None
    _db = None

    @classmethod
    def get_client(cls) -> AsyncIOMotorClient:
        if cls._client is None:
            mongo_url = os.getenv("MONGO_URL", "mongodb://mongo:27017")
            cls._client = AsyncIOMotorClient(mongo_url)
        return cls._client

    @classmethod
    def get_database(cls):
        if cls._db is None:
            cls._db = cls.get_client()[os.getenv("MONGO_DB_NAME", "celery_results")]
        return cls._db


async def get_mongo_collection(collection_name: str):
    db = MongoDB.get_database()
    return db[collection_name]
