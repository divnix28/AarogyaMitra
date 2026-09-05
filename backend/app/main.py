import sys
import os
import datetime

# 1. Add root Aarogyamitra directory to path BEFORE importing external modules
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))

from fastapi import FastAPI
from app.api.routes import chat, auth
from app.database.connection import engine
from app.models.learning import Base
from app.api.routes import chat
from channel_adaptor.Whatsapp.webhook import router as whatsapp_router

# 2. Initialize the FastAPI app first
app = FastAPI(
    title="AarogyaMitra AI Core Backend",
    description="Central orchestration layer for the AarogyaMitra AI ecosystem.",
    version="0.1.0"
)

Base.metadata.create_all(bind=engine)

# 3. Mount routers after the app is created
app.include_router(chat.router, prefix="/api/v1/chat", tags=["chat"])
app.include_router(auth.router, prefix="/api/v1/auth", tags=["auth"])

@app.get("/health")
async def health_check():
    return {"status": "healthy", "timestamp": datetime.datetime.now(datetime.timezone.utc)}
