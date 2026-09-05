from fastapi import FastAPI
import datetime
from app.database.connection import engine
from app.models.learning import Base
from app.api.routes import chat

app = FastAPI(
    title="AarogyaMitra AI Core Backend",
    description="Central orchestration layer for the AarogyaMitra AI ecosystem.",
    version="0.1.0"
)

Base.metadata.create_all(bind=engine)

app.include_router(chat.router, prefix="/api/v1/chat", tags=["chat"])

@app.get("/health")
async def health_check():
    return {"status": "healthy", "timestamp": datetime.datetime.now(datetime.timezone.utc)}
