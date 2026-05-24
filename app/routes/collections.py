from typing import Type, TypeVar
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel

from app.database import get_db
from app.auth import get_current_admin
from app.schemas.content import Skill, Project, Achievement, SocialLink, JournalEntry
from app.utils.objectid import stringify_id, stringify_list, to_object_id

router = APIRouter(prefix="/api", tags=["collections"])

T = TypeVar("T", bound=BaseModel)


def _make_crud(path: str, coll: str, model: Type[T], tag: str):
    sub = APIRouter()

    @sub.get(f"/{path}", response_model=list[model])  # type: ignore[valid-type]
    async def list_items():
        db = get_db()
        cursor = db[coll].find().sort([("order", 1), ("_id", 1)])
        docs = await cursor.to_list(length=500)
        return [model(**d) for d in stringify_list(docs)]

    @sub.post(f"/{path}", response_model=model)
    async def create_item(payload: model, _admin: dict = Depends(get_current_admin)):  # type: ignore[valid-type]
        db = get_db()
        data = payload.model_dump(exclude={"id"})
        res = await db[coll].insert_one(data)
        doc = await db[coll].find_one({"_id": res.inserted_id})
        return model(**stringify_id(doc))

    @sub.put(f"/{path}/{{item_id}}", response_model=model)
    async def update_item(item_id: str, payload: model, _admin: dict = Depends(get_current_admin)):  # type: ignore[valid-type]
        db = get_db()
        oid = to_object_id(item_id)
        data = payload.model_dump(exclude={"id"})
        res = await db[coll].update_one({"_id": oid}, {"$set": data})
        if res.matched_count == 0:
            raise HTTPException(status_code=404, detail=f"{tag} not found")
        doc = await db[coll].find_one({"_id": oid})
        return model(**stringify_id(doc))

    @sub.delete(f"/{path}/{{item_id}}")
    async def delete_item(item_id: str, _admin: dict = Depends(get_current_admin)):
        db = get_db()
        oid = to_object_id(item_id)
        res = await db[coll].delete_one({"_id": oid})
        if res.deleted_count == 0:
            raise HTTPException(status_code=404, detail=f"{tag} not found")
        return {"ok": True}

    return sub


router.include_router(_make_crud("skills", "skills", Skill, "Skill"))
router.include_router(_make_crud("projects", "projects", Project, "Project"))
router.include_router(_make_crud("achievements", "achievements", Achievement, "Achievement"))
router.include_router(_make_crud("social-links", "social_links", SocialLink, "Social link"))
router.include_router(_make_crud("journal", "journal", JournalEntry, "Journal entry"))
