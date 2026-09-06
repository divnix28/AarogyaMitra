import sys
import os
import datetime
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.routes import chat, auth, analytics  # Added analytics here
from app.database.connection import engine
from app.models.learning import Base
from channel_adaptor.Whatsapp.webhook import router as whatsapp_router

app = FastAPI(
    title="AarogyaMitra AI Core Backend",
    description="Central orchestration layer for the AarogyaMitra AI ecosystem.",
    version="0.1.0"
)

# Crucial for Member 6: Allows frontend (React/Vue) to make API calls to this backend
app.add_middleware(
    CORSMiddleware,
    allow_origin_regex=r"https?://(localhost|127\.0\.0\.1)(:\d+)?",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

Base.metadata.create_all(bind=engine)

app.include_router(chat.router, prefix="/api/v1/chat", tags=["chat"])
app.include_router(auth.router, prefix="/api/v1/auth", tags=["auth"])
app.include_router(analytics.router, prefix="/api/v1/analytics", tags=["analytics"]) # Mount new route
