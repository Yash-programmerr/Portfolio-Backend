from typing import Literal, Optional
from pydantic import BaseModel, Field, ConfigDict


EventType = Literal[
    "page_view",       # visitor landed
    "section_view",    # section entered viewport
    "section_dwell",   # cumulative time spent in section (sent on exit/unload)
    "click",           # generic click on something tracked
    "form_submit",     # contact form
    "resume_view",     # resume link opened
    "heartbeat",       # periodic ping while tab active
]


class EventIn(BaseModel):
    type: EventType
    target: Optional[str] = None         # e.g. "hero", "project:DemoCentra", "github"
    duration_ms: Optional[int] = None    # for section_dwell / heartbeat
    meta: Optional[dict] = None
    ts: Optional[str] = None             # client-side ISO timestamp


class IngestPayload(BaseModel):
    visitor_id: str = Field(min_length=8, max_length=64)
    session_id: str = Field(min_length=8, max_length=64)
    referrer: Optional[str] = None
    path: Optional[str] = "/"
    screen: Optional[str] = None         # e.g. "1920x1080"
    timezone: Optional[str] = None
    language: Optional[str] = None
    events: list[EventIn]


class SectionStat(BaseModel):
    name: str
    views: int = 0
    total_ms: int = 0


class Session(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    id: Optional[str] = None
    visitor_id: str
    session_id: str
    started_at: str
    last_activity_at: str
    path: Optional[str] = None
    referrer: Optional[str] = None
    ip: Optional[str] = None
    user_agent: Optional[str] = None
    screen: Optional[str] = None
    timezone: Optional[str] = None
    language: Optional[str] = None
    sections: list[SectionStat] = []
    clicks: list[dict] = []
    event_count: int = 0
    total_dwell_ms: int = 0


class Visitor(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    id: Optional[str] = None
    visitor_id: str
    first_seen: str
    last_seen: str
    session_count: int = 0
    total_dwell_ms: int = 0
    last_ip: Optional[str] = None
    last_user_agent: Optional[str] = None
    last_referrer: Optional[str] = None


class OverviewStats(BaseModel):
    total_visitors: int
    total_sessions: int
    sessions_today: int
    sessions_last_7d: int
    avg_dwell_ms: int
    top_sections: list[SectionStat]
