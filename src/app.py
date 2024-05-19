from fastapi import FastAPI
from config import settings
from services.database import sessionmanager
from api.client import router as client_router
from api.superadmin import router as superadmin_router
from api.admin import router as admin_router
from api.media import router as media_router
from api.all_roles import router as all_roles_router
from fastapi.middleware.cors import CORSMiddleware
from prometheus_fastapi_instrumentator import Instrumentator

sessionmanager.init(settings.DB_CONFIG)

app = FastAPI(title="Restaurant Table Reservation Server")


app.include_router(client_router, prefix="/api")
app.include_router(superadmin_router, prefix="/api")
app.include_router(admin_router, prefix="/api")
app.include_router(media_router, prefix="/api")
app.include_router(all_roles_router, prefix="/api")



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

Instrumentator().instrument(app).expose(app)
