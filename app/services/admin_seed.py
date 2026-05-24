from app.config import get_settings
from app.database import get_db
from app.auth import hash_password


async def ensure_admin_seed() -> None:
    settings = get_settings()
    db = get_db()
    email = settings.ADMIN_EMAIL.lower()
    existing = await db.users.find_one({"email": email})
    if existing:
        return
    await db.users.insert_one(
        {
            "email": email,
            "password_hash": hash_password(settings.ADMIN_PASSWORD),
            "role": "admin",
        }
    )
