from fastapi import FastAPI
from config import settings
from services.database import sessionmanager
from api.client import router as client_router
from api.superadmin import router as superadmin_router
from api.admin import router as admin_router

sessionmanager.init(settings.DB_CONFIG)

app = FastAPI(title="Restaurant Table Reservation Server")

app.include_router(client_router, prefix="/api")
app.include_router(superadmin_router, prefix="/api")
app.include_router(admin_router, prefix="/api")

