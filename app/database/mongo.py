from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase
from app.config import get_settings


class _DBState:
    client: AsyncIOMotorClient | None = None
    db: AsyncIOMotorDatabase | None = None


db_state = _DBState()


async def connect_to_mongo() -> None:
    settings = get_settings()
    db_state.client = AsyncIOMotorClient(settings.MONGODB_URI, serverSelectionTimeoutMS=8000)
    db_state.db = db_state.client[settings.MONGODB_DB]
    await db_state.client.admin.command("ping")


async def close_mongo_connection() -> None:
    if db_state.client is not None:
        db_state.client.close()
        db_state.client = None
        db_state.db = None


def get_db() -> AsyncIOMotorDatabase:
    if db_state.db is None:
        raise RuntimeError("MongoDB is not connected. Call connect_to_mongo() on startup.")
    return db_state.db
