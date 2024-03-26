from fastapi import FastAPI
from config import settings
from services.database import sessionmanager
from api.auth import router as auth_router

sessionmanager.init(settings.DB_CONFIG)


app = FastAPI(title="Restaurant Table Reservation Server")
app.include_router(auth_router, prefix="/api")

