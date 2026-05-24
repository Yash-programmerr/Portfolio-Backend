"""Idempotent seed: mirrors the current hardcoded portfolio content into MongoDB.

Run:
    python -m scripts.seed
"""
import asyncio
from app.database import connect_to_mongo, close_mongo_connection, get_db


HERO = {
    "_singleton": True,
    "badge_text": "Open to Opportunities",
    "name": "YASH",
    "roles": ["AI Developer", "Backend Engineer", "Full Stack Developer"],
    "headline_lines": [
        "Building intelligent",
        "systems with code and creativity",
    ],
    "subtext": (
        "Focused on RAG systems, AI-powered applications, scalable backend "
        "architecture, and immersive frontend experiences."
    ),
    "cta_primary_label": "Explore Projects",
    "cta_primary_target": "#projects",
    "cta_secondary_label": "Get In Touch",
    "cta_secondary_target": "#contact",
    "socials": [
        {"label": "GitHub", "href": "https://github.com/yash-programmerr"},
        {"label": "LinkedIn", "href": "https://www.linkedin.com/in/yashverma004/"},
    ],
    "tech_labels": [
        {"text": "AI Systems", "dot": "#00D4FF", "top": "12%", "left": "6%", "delay": 0, "float": "0s"},
        {"text": "RAG Pipelines", "dot": "#6C63FF", "top": "32%", "right": "4%", "delay": 0.15, "float": "1.3s"},
        {"text": "Backend Engineering", "dot": "#FFD700", "top": "53%", "left": "4%", "delay": 0.3, "float": "2.1s"},
        {"text": "Machine Learning", "dot": "#FF2D78", "bottom": "28%", "right": "5%", "delay": 0.1, "float": "0.7s"},
        {"text": "Interactive Frontend", "dot": "#00D4FF", "bottom": "10%", "left": "8%", "delay": 0.25, "float": "1.8s"},
    ],
    "profile_image": None,
}

ABOUT = {
    "_singleton": True,
    "headline_lines": ["Building systems", "that think,", "scale, and impress."],
    "paragraphs": [
        "I'm Yash Verma — an AI & Backend Engineer who builds intelligent systems that work in production. I combine deep backend architecture with AI capabilities to ship products that are fast, reliable, and genuinely smart.",
        "My stack lives at the intersection of LangChain, FastAPI, and pgvector on the backend — paired with Next.js and precision motion design on the front. Every system I build is designed for scale from day one.",
        "I'm obsessed with one question: how do we make software that genuinely understands context? That curiosity drives every RAG pipeline I architect and every API I design.",
    ],
    "quote": "Intelligence isn't about writing code — it's about understanding the problem deeply enough that the code becomes obvious.",
    "stats": [
        {"value": "2+", "label": "Years Building"},
        {"value": "5+", "label": "Projects Shipped"},
        {"value": "RAG", "label": "AI Specialization"},
        {"value": "∞", "label": "Curiosity"},
    ],
    "profile_name": "Yash Verma",
    "profile_role": "AI & Backend Engineer",
    "profile_image": "/profile.png",
    "available": True,
}

SKILLS = [
    {
        "name": "Langflow & N8N",
        "tagline": "AI Orchestration & RAG Architecture",
        "domain": "AI Systems",
        "accent": "#6C63FF",
        "wide": True,
        "what": [
            "End-to-end RAG pipeline design & deployment",
            "AI agent systems with tool use & memory",
            "Context-aware multi-turn conversational AI",
            "Multi-step reasoning & retrieval chains",
        ],
        "stack": ["Python", "Embeddings", "VectorDB", "Agents"],
        "order": 1,
    },
    {
        "name": "Gemini & HuggingFace APIs",
        "tagline": "LLM Integration & Prompt Engineering",
        "domain": "AI Systems",
        "accent": "#6C63FF",
        "wide": False,
        "what": [
            "Production LLM feature integration",
            "Semantic search via text embeddings",
            "Structured output & function calling",
            "Intelligent assistant architectures",
        ],
        "stack": ["GPT-4o", "Whisper", "Embeddings"],
        "order": 2,
    },
    {
        "name": "Python",
        "tagline": "AI Research & Backend Engineering",
        "domain": "Backend",
        "accent": "#00D4FF",
        "wide": False,
        "what": [
            "ML pipeline scripting & automation",
            "Data preprocessing & ETL workflows",
            "AI model integration & serving",
            "Backend automation & tooling",
        ],
        "stack": ["NumPy", "Pandas", "Asyncio", "Pydantic"],
        "order": 3,
    },
    {
        "name": "FastAPI",
        "tagline": "High-Performance Backend Infrastructure",
        "domain": "Backend",
        "accent": "#00D4FF",
        "wide": False,
        "what": [
            "Async AI model serving endpoints",
            "Real-time data streaming APIs",
            "Scalable microservice design",
            "Background task & queue systems",
        ],
        "stack": ["Python", "Async", "REST", "WebSockets"],
        "order": 4,
    },
    {
        "name": "PostgreSQL & MongoDB",
        "tagline": "Relational & Vector Database Architecture",
        "domain": "Backend",
        "accent": "#00D4FF",
        "wide": False,
        "what": [
            "Complex relational data modeling",
            "pgvector for semantic similarity search",
            "Query optimization & indexing strategies",
            "Scalable backend data layer design",
        ],
        "stack": ["pgvector", "SQL", "Indexing", "Migrations"],
        "order": 5,
    },
    {
        "name": "Node.js",
        "tagline": "Real-Time Backend Systems",
        "domain": "Backend",
        "accent": "#00D4FF",
        "wide": False,
        "what": [
            "Real-time WebSocket API infrastructure",
            "Event-driven microservice architecture",
            "RESTful API design & middleware layers",
            "Server-side AI feature orchestration",
        ],
        "stack": ["Express", "WebSocket", "TypeScript", "JWT"],
        "order": 6,
    },
    {
        "name": "React.js",
        "tagline": "Interactive Frontend Systems",
        "domain": "Frontend",
        "accent": "#61DAFB",
        "wide": False,
        "what": [
            "Dynamic component-driven user interfaces",
            "Interactive AI-powered frontend experiences",
            "Real-time state management & UI rendering",
            "Responsive modern application architecture",
        ],
        "stack": ["React", "Next.js", "TypeScript", "Tailwind CSS"],
        "order": 7,
    },
]

PROJECTS = [
    {
        "title": "DemoCentra",
        "subtitle": "AI-Powered Civic Intelligence Platform",
        "description": "A next-generation civic reporting platform designed to streamline public issue reporting through AI-assisted workflows, intelligent categorization, real-time tracking, and modern citizen engagement systems.",
        "tags": ["React.js", "FastAPI", "PostgreSQL", "Gemini", "AI Workflows"],
        "accent": "#6C63FF",
        "gradient": "from-[#6C63FF] to-[#00D4FF]",
        "year": "2025",
        "status": "In Progress",
        "highlights": [
            "AI-assisted issue classification",
            "Real-time civic reporting system",
            "Smart workflow automation",
            "Interactive citizen dashboard",
        ],
        "order": 1,
    },
    {
        "title": "RAG Chatbot",
        "subtitle": "Context-Aware Conversational AI",
        "description": "Production-ready retrieval-augmented chatbot that ingests custom document corpora, performs semantic search via embeddings, and delivers grounded responses at scale.",
        "tags": ["Python", "LangChain", "FastAPI"],
        "accent": "#00D4FF",
        "gradient": "from-[#00D4FF] to-[#6C63FF]",
        "year": "2024",
        "status": "Live",
        "highlights": ["Multi-format ingestion", "Semantic chunking", "Streaming responses", "Citation tracking"],
        "order": 2,
    },
    {
        "title": "ComradeX",
        "subtitle": "Personal Intelligence for Learning",
        "description": "An intelligent study companion that analyzes uploaded materials, generates flashcards, creates study schedules, and uses spaced-repetition algorithms for optimal retention.",
        "tags": ["React.js", "Gemini", "PostgreSQL", "FastAPI"],
        "accent": "#FF2D78",
        "gradient": "from-[#FF2D78] to-[#FF8C00]",
        "year": "2024",
        "status": "In Progress",
        "highlights": ["Spaced repetition", "AI flashcard generation", "Study analytics", "Personalized scheduling"],
        "order": 3,
    },
    {
        "title": "NEXORA",
        "subtitle": "Multimodal AI Verification Infrastructure",
        "description": "A next-generation AI intelligence platform built to detect misinformation across text, audio, and video mediums using multimodal analysis, contextual verification pipelines, and scalable backend systems designed to reduce public panic and improve civic trust.",
        "tags": ["React.js", "FastAPI", "PostgreSQL", "Gemini Multimodal API"],
        "accent": "#FF2D78",
        "gradient": "from-[#FF2D78] to-[#FF8C00]",
        "year": "2025",
        "status": "In Progress",
        "highlights": [
            "AI-powered multimodal verification",
            "Real-time misinformation analysis",
            "Context-aware media intelligence",
            "Scalable civic communication system",
        ],
        "order": 4,
    },
]

HACKATHONS = [
    {
        "name": "Smart India Hackathon",
        "achievement": "Institute Nominee Team",
        "year": "2025",
        "description": "Pokango is a comprehensive web-based travel tracking platform designed to capture, analyze, and store detailed trip information for transportation research and urban planning purposes.",
        "techStack": ["Gemini API", "Google Mapbox API", "Express.js", "Node.js", "React"],
        "icon": "🚀",
        "accent": "#FFD700",
    },
    {
        "name": "Mumbai Hacks",
        "achievement": "Semi-Finalist",
        "year": "2025",
        "description": "Nexora is an AI-powered, multi-agent platform that combats misinformation across text, image, and video domains using an orchestrated system of intelligent agents.",
        "techStack": ["TypeScript", "Next.js", "OpenAI", "Gemini API", "Redis"],
        "icon": "🚀",
        "accent": "#6C63FF",
    },
    {
        "name": "India Innovates",
        "achievement": "Semi-Finalist",
        "year": "2026",
        "description": "DemoCentra is an AI-powered digital governance platform that efficiently manages citizen complaints, automates government workflows, and improves governance transparency.",
        "techStack": ["React", "Gemini API", "MongoDB", "Express.js", "OCR", "Node.js"],
        "icon": "🚀",
        "accent": "#00D4FF",
    },
    {
        "name": "Tech Sagethon",
        "achievement": "Semi-Finalist",
        "year": "2026",
        "description": "An AI-powered platform that bridges the gap between student academics, technical skills, and career opportunities through intelligent analytics and personalized recommendations.",
        "techStack": ["React", "LangFlow", "N8N", "MongoDB", "Scikit-Learn", "Python", "FastAPI"],
        "icon": "🚀",
        "accent": "#00D4FF",
    },
    {
        "name": "TIT Srijan",
        "achievement": "Semi-Finalist",
        "year": "2026",
        "description": "ComradeX an AI-powered LMS learning assistant integrated with a video player using RAG-based contextual understanding.",
        "techStack": ["React", "Langchain", "N8N", "MongoDB", "Scikit-Learn", "Python", "FastAPI", "RAG Modelling"],
        "icon": "🚀",
        "accent": "#00D4FF",
    },
]

ACHIEVEMENTS = [
    {
        "icon": "🤖",
        "category": "AI Development",
        "title": "Built Production AI LMS",
        "description": "Designed and built RAG pipelines with langchain and Fast, for adaptive quizzing, and real-time analytics used by real learners.",
        "date": "2024",
        "accent": "#6C63FF",
        "size": "lg",
        "is_hackathon": False,
        "hackathons": [],
        "order": 1,
    },
    {
        "icon": "⚡",
        "category": "Hackathon",
        "title": "Hackathon Finalist & Winner",
        "description": "Competed in multiple hackathons building AI-powered solutions under intense time constraints.",
        "date": "2025-present",
        "accent": "#FFD700",
        "size": "sm",
        "is_hackathon": True,
        "hackathons": HACKATHONS,
        "order": 2,
    },
    {
        "icon": "🎓",
        "category": "Certification",
        "title": "AI & ML Certifications",
        "description": "Completed professional certifications in machine learning, LLM engineering, and full-stack development from industry-recognized platforms.",
        "date": "2023–present",
        "accent": "#00D4FF",
        "size": "sm",
        "is_hackathon": False,
        "hackathons": [],
        "order": 3,
    },
    {
        "icon": "🦜",
        "category": "AI Engineering",
        "title": "RAG Systems at Scale",
        "description": "Architected and deployed multiple retrieval-augmented generation pipelines with sub-second semantic search across large document corpora.",
        "date": "2026",
        "accent": "#00D4FF",
        "size": "sm",
        "is_hackathon": False,
        "hackathons": [],
        "order": 4,
    },
    {
        "icon": "💻",
        "category": "Milestone",
        "title": "500+ Coding Hours",
        "description": "Consistent deep work building complex systems — AI backends, motion-rich frontends, and full-stack applications across varied domains.",
        "date": "2023–2026",
        "accent": "#6C63FF",
        "size": "sm",
        "is_hackathon": False,
        "hackathons": [],
        "order": 5,
    },
    {
        "icon": "📐",
        "category": "Academic",
        "title": "Computer Science Foundation",
        "description": "Strong academic grounding in algorithms, data structures, and systems — combined with real-world project experience building production software.",
        "date": "2023–present",
        "accent": "#FF2D78",
        "size": "sm",
        "is_hackathon": False,
        "hackathons": [],
        "order": 6,
    },
]

SITE_META = {
    "_singleton": True,
    "achievements_counters": [
        {"value": "8", "suffix": "+", "label": "Projects Built"},
        {"value": "5", "suffix": "+", "label": "AI Systems"},
        {"value": "5", "suffix": "x", "label": "Hackathon Participant"},
        {"value": "500", "suffix": "+", "label": "Hours of Coding"},
    ],
    "skills_ticker": [
        "LangChain", "FastAPI", "React", "Python", "PostgreSQL",
        "MongoDB", "SQL", "Gemini API", "Node.js", "RAG Systems", "Docker",
    ],
    "skills_domains": [
        {"label": "AI Systems", "color": "#6C63FF"},
        {"label": "Backend Infrastructure", "color": "#00D4FF"},
        {"label": "Frontend Engineering", "color": "#FFD700"},
        {"label": "Motion & Visual", "color": "#FF2D78"},
    ],
    "skills_bottom_counters": [
        {"value": "10", "suffix": "+", "label": "Technologies"},
        {"value": "4", "suffix": "", "label": "Engineering Domains"},
        {"value": "RAG", "suffix": "", "label": "AI Specialization"},
        {"value": "Full Stack", "suffix": "", "label": "End-to-End"},
    ],
    "footer_brand_letter": "Y",
    "footer_brand_rest": "ash",
    "footer_tagline": "AI & Backend Engineer",
    "footer_signature": "Built with Next.js + GSAP",
}

SOCIAL_LINKS = [
    {
        "platform": "GitHub",
        "label": "GitHub : Yash-programmerr",
        "href": "https://github.com/Yash-programmerr",
        "icon_key": "github",
        "order": 1,
    },
    {
        "platform": "LinkedIn",
        "label": "LinkedIn : Yash Verma",
        "href": "https://www.linkedin.com/in/yashverma004/",
        "icon_key": "linkedin",
        "order": 2,
    },
    {
        "platform": "Email",
        "label": "Email : vermayash2200@gmail.com",
        "href": "mailto:vermayash2200@gmail.com",
        "icon_key": "email",
        "order": 3,
    },
]


async def upsert_singleton(coll, doc: dict) -> None:
    await coll.update_one({"_singleton": True}, {"$set": doc}, upsert=True)


async def upsert_list(coll, docs: list[dict], key: str) -> None:
    for d in docs:
        await coll.update_one({key: d[key]}, {"$set": d}, upsert=True)


async def main() -> None:
    await connect_to_mongo()
    db = get_db()
    await upsert_singleton(db.hero, HERO)
    await upsert_singleton(db.about, ABOUT)
    await upsert_singleton(db.site_meta, SITE_META)
    await upsert_list(db.skills, SKILLS, key="name")
    await upsert_list(db.projects, PROJECTS, key="title")
    await upsert_list(db.achievements, ACHIEVEMENTS, key="title")
    await upsert_list(db.social_links, SOCIAL_LINKS, key="platform")
    print("Seed complete.")
    await close_mongo_connection()


if __name__ == "__main__":
    asyncio.run(main())
