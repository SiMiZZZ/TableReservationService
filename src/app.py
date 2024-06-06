from fastapi import FastAPI
from config import settings
from services.database import sessionmanager
from api.client import router as client_router
from api.superadmin import router as superadmin_router
from api.admin import router as admin_router
from api.ws import router as ws_router
from api.all_roles import router as all_roles_router
from fastapi.middleware.cors import CORSMiddleware
from prometheus_fastapi_instrumentator import Instrumentator
from typing import Optional

from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi import FastAPI

from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from fastapi_cache.decorator import cache

from redis import asyncio as aioredis

sessionmanager.init(settings.DB_CONFIG)

app = FastAPI(title="Restaurant Table Reservation Server")


app.include_router(client_router, prefix="/api")
app.include_router(superadmin_router, prefix="/api")
app.include_router(admin_router, prefix="/api")
app.include_router(all_roles_router, prefix="/api")
app.include_router(ws_router, prefix="/ws")

origins = [
    "*"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@asynccontextmanager
async def lifespan(_: FastAPI) -> AsyncIterator[None]:
    redis = aioredis.from_url("redis://redis")
    FastAPICache.init(RedisBackend(redis), prefix="fastapi-cache")
    yield

Instrumentator().instrument(app).expose(app)
