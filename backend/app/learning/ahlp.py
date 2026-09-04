from pydantic import BaseModel
from typing import List, Optional
from enum import Enum

class KnowledgeLevel(str, Enum):
    NOVICE = "NOVICE"
    INTERMEDIATE = "INTERMEDIATE"
    ADVANCED = "ADVANCED"

class BehaviourStage(str, Enum):
    AWARENESS = "AWARENESS"
    PREPARATION = "PREPARATION"
    ACTION = "ACTION"
    MAINTENANCE = "MAINTENANCE"

class AHLPProfile(BaseModel):
    user_id: str
    preferred_language: str = "en"
    knowledge_level: KnowledgeLevel = KnowledgeLevel.NOVICE
    behaviour_stage: BehaviourStage = BehaviourStage.AWARENESS
    identified_misconceptions: List[str] = []
    completed_topics: List[str] = []

def update_profile_knowledge(profile: AHLPProfile, new_level: KnowledgeLevel) -> AHLPProfile:
    profile.knowledge_level = new_level
    return profile