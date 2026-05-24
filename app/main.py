from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from slowapi.middleware import SlowAPIMiddleware

from app.config import get_settings
from app.database import connect_to_mongo, close_mongo_connection
from app.services.admin_seed import ensure_admin_seed
from app.middleware.rate_limit import limiter
from app.routes import auth as auth_routes
from app.routes import singletons as singleton_routes
from app.routes import collections as collection_routes
from app.routes import messages as messages_routes
from app.routes import analytics as analytics_routes


@asynccontextmanager
async def lifespan(_: FastAPI):
    await connect_to_mongo()
    await ensure_admin_seed()
    yield
    await close_mongo_connection()


settings = get_settings()

app = FastAPI(title="Yash Portfolio API", version="1.0.0", lifespan=lifespan)

# Rate limiting (per-IP, in-memory)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)
app.add_middleware(SlowAPIMiddleware)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origin_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/api/health")
async def health():
    return {"status": "ok"}


app.include_router(auth_routes.router)
app.include_router(singleton_routes.router)
app.include_router(collection_routes.router)
app.include_router(messages_routes.router)
app.include_router(analytics_routes.router)
