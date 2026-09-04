from pydantic import BaseModel
from typing import Dict, List

class CampaignInteraction(BaseModel):
    campaign_id: str
    interaction_type: str  # e.g., "viewed", "clicked", "completed"

def calculate_campaign_engagement(interactions: List[CampaignInteraction]) -> Dict[str, Dict[str, int]]:
    # Tracks engagement metrics per campaign without tracking individual users
    metrics = {}
    for interaction in interactions:
        cid = interaction.campaign_id
        itype = interaction.interaction_type
        
        if cid not in metrics:
            metrics[cid] = {"viewed": 0, "clicked": 0, "completed": 0}
            
        if itype in metrics[cid]:
            metrics[cid][itype] += 1
            
    return metrics