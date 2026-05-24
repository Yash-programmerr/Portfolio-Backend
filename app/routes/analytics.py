from datetime import datetime, timezone, timedelta
from fastapi import APIRouter, Depends, HTTPException, Request
from pymongo import ReturnDocument

from app.database import get_db
from app.auth import get_current_admin
from app.middleware.rate_limit import limiter
from app.schemas.analytics import (
    IngestPayload, Session, Visitor, OverviewStats, SectionStat,
)
from app.utils.objectid import stringify_id, stringify_list, to_object_id

router = APIRouter(prefix="/api/analytics", tags=["analytics"])


def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


# ── PUBLIC INGEST ─────────────────────────────────────────────
@router.post("/ingest")
@limiter.limit("120/minute")
async def ingest(request: Request, payload: IngestPayload):
    """Public endpoint — frontend sends batched events here.
    Rate-limited to 120 batches per minute per IP (real visitors send ~8 per minute)."""
    db = get_db()
    now = _now_iso()
    ip = request.client.host if request.client else None
    ua = request.headers.get("user-agent")

    # ── 1) Upsert visitor (rollup per browser) ────────────────
    await db.visitors.update_one(
        {"visitor_id": payload.visitor_id},
        {
            "$setOnInsert": {"visitor_id": payload.visitor_id, "first_seen": now, "session_count": 0, "total_dwell_ms": 0},
            "$set": {"last_seen": now, "last_ip": ip, "last_user_agent": ua, "last_referrer": payload.referrer},
        },
        upsert=True,
    )

    # ── 2) Find/create the session doc ────────────────────────
    existing = await db.sessions.find_one({"session_id": payload.session_id})
    if not existing:
        await db.sessions.insert_one({
            "visitor_id": payload.visitor_id,
            "session_id": payload.session_id,
            "started_at": now,
            "last_activity_at": now,
            "path": payload.path,
            "referrer": payload.referrer,
            "ip": ip,
            "user_agent": ua,
            "screen": payload.screen,
            "timezone": payload.timezone,
            "language": payload.language,
            "sections": [],
            "clicks": [],
            "event_count": 0,
            "total_dwell_ms": 0,
        })
        # bump session_count on visitor
        await db.visitors.update_one(
            {"visitor_id": payload.visitor_id},
            {"$inc": {"session_count": 1}},
        )
        existing = await db.sessions.find_one({"session_id": payload.session_id})

    # ── 3) Apply batched events ───────────────────────────────
    sections: dict[str, dict] = {s["name"]: dict(s) for s in existing.get("sections", [])}
    clicks: list[dict] = list(existing.get("clicks", []))
    dwell_added = 0
    event_count_added = 0

    for ev in payload.events:
        event_count_added += 1

        if ev.type == "section_view" and ev.target:
            sec = sections.setdefault(ev.target, {"name": ev.target, "views": 0, "total_ms": 0})
            sec["views"] += 1

        elif ev.type == "section_dwell" and ev.target and ev.duration_ms:
            sec = sections.setdefault(ev.target, {"name": ev.target, "views": 0, "total_ms": 0})
            sec["total_ms"] += ev.duration_ms
            dwell_added += ev.duration_ms

        elif ev.type == "click" and ev.target:
            clicks.append({
                "target": ev.target,
                "meta": ev.meta or {},
                "ts": ev.ts or _now_iso(),
            })

        elif ev.type in ("form_submit", "resume_view") and ev.target is not None:
            clicks.append({
                "target": f"{ev.type}:{ev.target or ev.type}",
                "meta": ev.meta or {},
                "ts": ev.ts or _now_iso(),
            })

        # page_view / heartbeat just bump last_activity_at + counts

    await db.sessions.update_one(
        {"session_id": payload.session_id},
        {
            "$set": {
                "last_activity_at": now,
                "sections": list(sections.values()),
                "clicks": clicks[-200:],  # cap for safety
            },
            "$inc": {
                "event_count": event_count_added,
                "total_dwell_ms": dwell_added,
            },
        },
    )
    if dwell_added:
        await db.visitors.update_one(
            {"visitor_id": payload.visitor_id},
            {"$inc": {"total_dwell_ms": dwell_added}},
        )

    return {"ok": True, "events_ingested": event_count_added}


# ── ADMIN: OVERVIEW ───────────────────────────────────────────
@router.get("/overview", response_model=OverviewStats)
async def overview(_admin: dict = Depends(get_current_admin)):
    db = get_db()
    total_visitors = await db.visitors.count_documents({})
    total_sessions = await db.sessions.count_documents({})

    now = datetime.now(timezone.utc)
    today_start = now.replace(hour=0, minute=0, second=0, microsecond=0).isoformat()
    seven_days_ago = (now - timedelta(days=7)).isoformat()

    sessions_today = await db.sessions.count_documents({"started_at": {"$gte": today_start}})
    sessions_last_7d = await db.sessions.count_documents({"started_at": {"$gte": seven_days_ago}})

    # avg dwell
    pipeline = [{"$group": {"_id": None, "avg": {"$avg": "$total_dwell_ms"}}}]
    agg = await db.sessions.aggregate(pipeline).to_list(length=1)
    avg_dwell_ms = int(agg[0]["avg"]) if agg and agg[0].get("avg") else 0

    # top sections (aggregate across sessions)
    sec_pipeline = [
        {"$unwind": "$sections"},
        {"$group": {
            "_id": "$sections.name",
            "views": {"$sum": "$sections.views"},
            "total_ms": {"$sum": "$sections.total_ms"},
        }},
        {"$sort": {"total_ms": -1}},
        {"$limit": 10},
    ]
    sec_agg = await db.sessions.aggregate(sec_pipeline).to_list(length=10)
    top_sections = [
        SectionStat(name=s["_id"], views=int(s["views"]), total_ms=int(s["total_ms"]))
        for s in sec_agg
    ]

    return OverviewStats(
        total_visitors=total_visitors,
        total_sessions=total_sessions,
        sessions_today=sessions_today,
        sessions_last_7d=sessions_last_7d,
        avg_dwell_ms=avg_dwell_ms,
        top_sections=top_sections,
    )


# ── ADMIN: VISITORS LIST ──────────────────────────────────────
@router.get("/visitors", response_model=list[Visitor])
async def list_visitors(_admin: dict = Depends(get_current_admin), limit: int = 100):
    db = get_db()
    cursor = db.visitors.find().sort("last_seen", -1).limit(min(limit, 500))
    docs = await cursor.to_list(length=limit)
    return [Visitor(**d) for d in stringify_list(docs)]


# ── ADMIN: SESSIONS FOR A VISITOR ─────────────────────────────
@router.get("/visitors/{visitor_id}/sessions", response_model=list[Session])
async def sessions_for_visitor(visitor_id: str, _admin: dict = Depends(get_current_admin)):
    db = get_db()
    cursor = db.sessions.find({"visitor_id": visitor_id}).sort("started_at", -1)
    docs = await cursor.to_list(length=200)
    return [Session(**d) for d in stringify_list(docs)]


# ── ADMIN: SINGLE SESSION DETAIL ──────────────────────────────
@router.get("/sessions/{session_id}", response_model=Session)
async def session_detail(session_id: str, _admin: dict = Depends(get_current_admin)):
    db = get_db()
    doc = await db.sessions.find_one({"session_id": session_id})
    if not doc:
        raise HTTPException(status_code=404, detail="Session not found")
    return Session(**stringify_id(doc))


# ── ADMIN: DELETE VISITOR (and all their sessions) ────────────
@router.delete("/visitors/{visitor_id}")
async def delete_visitor(visitor_id: str, _admin: dict = Depends(get_current_admin)):
    db = get_db()
    await db.sessions.delete_many({"visitor_id": visitor_id})
    res = await db.visitors.delete_one({"visitor_id": visitor_id})
    return {"ok": True, "deleted": res.deleted_count}
