from typing import Any
from bson import ObjectId


def stringify_id(doc: dict | None) -> dict | None:
    if doc is None:
        return None
    if "_id" in doc:
        doc["id"] = str(doc.pop("_id"))
    return doc


def stringify_list(docs: list[dict]) -> list[dict]:
    return [stringify_id(d) for d in docs]


def to_object_id(value: str) -> ObjectId:
    try:
        return ObjectId(value)
    except Exception as exc:
        from fastapi import HTTPException
        raise HTTPException(status_code=400, detail=f"Invalid id: {value}") from exc
