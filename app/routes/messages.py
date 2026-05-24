from datetime import datetime, timezone
from fastapi import APIRouter, Depends, HTTPException, Request
from app.database import get_db
from app.auth import get_current_admin
from app.middleware.rate_limit import limiter
from app.schemas.content import Message, MessageCreate
from app.utils.objectid import stringify_id, stringify_list, to_object_id

router = APIRouter(prefix="/api/messages", tags=["messages"])


@router.post("", response_model=Message)
@limiter.limit("5/hour")
async def submit_message(request: Request, payload: MessageCreate):
    """Public — anyone can submit a contact form message.
    Rate-limited to 5 submissions per hour per IP (anti-spam)."""
    db = get_db()
    doc = {
        "name": payload.name.strip(),
        "email": payload.email.strip().lower(),
        "message": payload.message.strip(),
        "created_at": datetime.now(timezone.utc).isoformat(),
        "read": False,
        "ip": (request.client.host if request.client else None),
        "user_agent": request.headers.get("user-agent"),
    }
    res = await db.messages.insert_one(doc)
    saved = await db.messages.find_one({"_id": res.inserted_id})
    return Message(**stringify_id(saved))


@router.get("", response_model=list[Message])
async def list_messages(_admin: dict = Depends(get_current_admin)):
    db = get_db()
    cursor = db.messages.find().sort("_id", -1)
    docs = await cursor.to_list(length=500)
    return [Message(**d) for d in stringify_list(docs)]


@router.patch("/{message_id}/read", response_model=Message)
async def mark_read(message_id: str, _admin: dict = Depends(get_current_admin)):
    db = get_db()
    oid = to_object_id(message_id)
    res = await db.messages.update_one({"_id": oid}, {"$set": {"read": True}})
    if res.matched_count == 0:
        raise HTTPException(status_code=404, detail="Message not found")
    doc = await db.messages.find_one({"_id": oid})
    return Message(**stringify_id(doc))


@router.delete("/{message_id}")
async def delete_message(message_id: str, _admin: dict = Depends(get_current_admin)):
    db = get_db()
    res = await db.messages.delete_one({"_id": to_object_id(message_id)})
    if res.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Message not found")
    return {"ok": True}
