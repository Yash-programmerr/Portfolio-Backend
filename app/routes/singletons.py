from fastapi import APIRouter, Depends
from app.database import get_db
from app.auth import get_current_admin
from app.schemas.content import Hero, About, Resume, SiteMeta
from app.utils.objectid import stringify_id

router = APIRouter(prefix="/api", tags=["singletons"])


# ── Hero ──────────────────────────────────────────────────────
@router.get("/hero", response_model=Hero)
async def get_hero():
    db = get_db()
    doc = await db.hero.find_one({"_singleton": True}) or {}
    return Hero(**stringify_id(doc) or {})


@router.put("/hero", response_model=Hero)
async def update_hero(payload: Hero, _admin: dict = Depends(get_current_admin)):
    db = get_db()
    data = payload.model_dump(exclude={"id"}, by_alias=True)
    data["_singleton"] = True
    await db.hero.update_one({"_singleton": True}, {"$set": data}, upsert=True)
    doc = await db.hero.find_one({"_singleton": True})
    return Hero(**stringify_id(doc))


# ── About ─────────────────────────────────────────────────────
@router.get("/about", response_model=About)
async def get_about():
    db = get_db()
    doc = await db.about.find_one({"_singleton": True}) or {}
    return About(**stringify_id(doc) or {})


@router.put("/about", response_model=About)
async def update_about(payload: About, _admin: dict = Depends(get_current_admin)):
    db = get_db()
    data = payload.model_dump(exclude={"id"})
    data["_singleton"] = True
    await db.about.update_one({"_singleton": True}, {"$set": data}, upsert=True)
    doc = await db.about.find_one({"_singleton": True})
    return About(**stringify_id(doc))


# ── Site Meta ─────────────────────────────────────────────────
@router.get("/site-meta", response_model=SiteMeta)
async def get_site_meta():
    db = get_db()
    doc = await db.site_meta.find_one({"_singleton": True}) or {}
    return SiteMeta(**stringify_id(doc) or {})


@router.put("/site-meta", response_model=SiteMeta)
async def update_site_meta(payload: SiteMeta, _admin: dict = Depends(get_current_admin)):
    db = get_db()
    data = payload.model_dump(exclude={"id"})
    data["_singleton"] = True
    await db.site_meta.update_one({"_singleton": True}, {"$set": data}, upsert=True)
    doc = await db.site_meta.find_one({"_singleton": True})
    return SiteMeta(**stringify_id(doc))


# ── Resume ────────────────────────────────────────────────────
@router.get("/resume", response_model=Resume)
async def get_resume():
    db = get_db()
    doc = await db.resume.find_one({"_singleton": True}) or {}
    return Resume(**stringify_id(doc) or {})


@router.put("/resume", response_model=Resume)
async def update_resume(payload: Resume, _admin: dict = Depends(get_current_admin)):
    db = get_db()
    data = payload.model_dump(exclude={"id"})
    data["_singleton"] = True
    await db.resume.update_one({"_singleton": True}, {"$set": data}, upsert=True)
    doc = await db.resume.find_one({"_singleton": True})
    return Resume(**stringify_id(doc))
