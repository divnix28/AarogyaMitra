from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Bypassing Docker: Using local SQLite for unblocked development
SQLALCHEMY_DATABASE_URL = "sqlite:///./aarogyamitra.db"

# connect_args={"check_same_thread": False} is required for SQLite in FastAPI
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()