from sqlalchemy import Column, Integer, String, Float, JSON, DateTime
from sqlalchemy.ext.declarative import declarative_base
import datetime

Base = declarative_base()

class AdaptiveLearningProfile(Base):
    __tablename__ = "learning_profiles"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String, unique=True, index=True)
    preferred_language = Column(String, default="hi")
    knowledge_level = Column(String, default="beginner")
    behaviour_stage = Column(String, default="awareness")
    misconceptions_tracked = Column(JSON, default=list)
    retention_score = Column(Float, default=0.0)
    last_interaction = Column(DateTime, default=datetime.datetime.now(datetime.timezone.utc))

class TeachBackAttempt(Base):
    __tablename__ = "teachback_attempts"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String, index=True)
    topic = Column(String, index=True)
    understanding_status = Column(String)
    timestamp = Column(DateTime, default=datetime.datetime.now(datetime.timezone.utc))
