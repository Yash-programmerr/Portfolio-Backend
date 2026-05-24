from typing import Literal, Optional
from pydantic import BaseModel, Field, ConfigDict


# ── shared mixin ──────────────────────────────────────────────
class MongoModel(BaseModel):
    model_config = ConfigDict(populate_by_name=True, str_strip_whitespace=True)
    id: Optional[str] = None


# ── HERO ──────────────────────────────────────────────────────
class TechLabel(BaseModel):
    text: str
    dot: str = "#6C63FF"
    top: Optional[str] = None
    right: Optional[str] = None
    bottom: Optional[str] = None
    left: Optional[str] = None
    delay: float = 0
    float_offset: str = Field("0s", alias="float")
    model_config = ConfigDict(populate_by_name=True)


class HeroSocial(BaseModel):
    label: str
    href: str


class Hero(MongoModel):
    badge_text: str = "Open to Opportunities"
    name: str = "YASH"
    roles: list[str] = []
    headline_lines: list[str] = []
    subtext: str = ""
    cta_primary_label: str = "Explore Projects"
    cta_primary_target: str = "#projects"
    cta_secondary_label: str = "Get In Touch"
    cta_secondary_target: str = "#contact"
    socials: list[HeroSocial] = []
    tech_labels: list[TechLabel] = []
    profile_image: Optional[str] = None


# ── ABOUT ─────────────────────────────────────────────────────
class StatItem(BaseModel):
    value: str
    label: str


class About(MongoModel):
    headline_lines: list[str] = []
    paragraphs: list[str] = []
    quote: str = ""
    stats: list[StatItem] = []
    profile_name: str = "Yash Verma"
    profile_role: str = "AI & Backend Engineer"
    profile_image: Optional[str] = None
    available: bool = True


# ── SKILLS ────────────────────────────────────────────────────
class Skill(MongoModel):
    name: str
    tagline: str = ""
    domain: str = "Backend"
    accent: str = "#6C63FF"
    wide: bool = False
    what: list[str] = []
    stack: list[str] = []
    order: int = 0


# ── PROJECTS ──────────────────────────────────────────────────
ProjectStatus = Literal["Live", "In Progress", "Concept"]


class Project(MongoModel):
    title: str
    subtitle: str = ""
    description: str = ""
    tags: list[str] = []
    accent: str = "#6C63FF"
    gradient: str = "from-[#6C63FF] to-[#00D4FF]"
    year: str = ""
    status: ProjectStatus = "In Progress"
    link: Optional[str] = None
    github: Optional[str] = None
    thumbnail: Optional[str] = None
    highlights: list[str] = []
    order: int = 0


# ── ACHIEVEMENTS ──────────────────────────────────────────────
AchSize = Literal["lg", "sm"]


class HackathonItem(BaseModel):
    name: str
    achievement: str
    year: str
    description: str = ""
    techStack: list[str] = []
    icon: str = "🚀"
    accent: str = "#6C63FF"


class Achievement(MongoModel):
    icon: str = "🏆"
    category: str = ""
    title: str
    description: str = ""
    date: str = ""
    accent: str = "#6C63FF"
    size: AchSize = "sm"
    is_hackathon: bool = False
    hackathons: list[HackathonItem] = []
    order: int = 0


# ── SOCIAL LINKS (footer / contact) ───────────────────────────
class SocialLink(MongoModel):
    platform: str
    label: str
    href: str
    icon_key: str = "link"
    order: int = 0


# ── RESUME ────────────────────────────────────────────────────
class Resume(MongoModel):
    url: str = ""
    updated_at: Optional[str] = None


# ── SITE META (counters, ticker, domains, footer) ─────────────
class Counter(BaseModel):
    value: str
    label: str
    suffix: Optional[str] = None


class Domain(BaseModel):
    label: str
    color: str = "#6C63FF"


class SiteMeta(MongoModel):
    achievements_counters: list[Counter] = []
    skills_ticker: list[str] = []
    skills_domains: list[Domain] = []
    skills_bottom_counters: list[Counter] = []
    footer_brand_letter: str = "Y"
    footer_brand_rest: str = "ash"
    footer_tagline: str = "AI & Backend Engineer"
    footer_signature: str = "Built with Next.js + GSAP"


# ── JOURNAL ENTRIES ───────────────────────────────────────────
JournalType = Literal["research", "workshop", "seminar", "event"]


class ProofLink(BaseModel):
    label: str
    url: str
    kind: str = "external"   # "certificate" | "pdf" | "video" | "external"


class JournalEntry(MongoModel):
    title: str
    entry_type: JournalType = "event"
    date: str = ""                # ISO "YYYY-MM-DD"
    location: Optional[str] = None
    organization: Optional[str] = None
    role: Optional[str] = None
    description: str = ""
    cover_image: Optional[str] = None
    images: list[str] = []
    proof_links: list[ProofLink] = []
    tags: list[str] = []
    accent: str = "#6C63FF"
    featured: bool = False
    order: int = 0


# ── CONTACT MESSAGES ──────────────────────────────────────────
class MessageCreate(BaseModel):
    name: str = Field(min_length=1, max_length=120)
    email: str = Field(min_length=3, max_length=200)
    message: str = Field(min_length=1, max_length=5000)


class Message(MongoModel):
    name: str
    email: str
    message: str
    created_at: Optional[str] = None
    read: bool = False
    ip: Optional[str] = None
    user_agent: Optional[str] = None
