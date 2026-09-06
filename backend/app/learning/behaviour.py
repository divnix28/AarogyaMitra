from .ahlp import BehaviourStage, AHLPProfile

def calculate_progression(profile: AHLPProfile, positive_actions_logged: int) -> BehaviourStage:
    if positive_actions_logged >= 5:
        return BehaviourStage.MAINTENANCE
    elif positive_actions_logged >= 3:
        return BehaviourStage.ACTION
    elif positive_actions_logged >= 1:
        return BehaviourStage.PREPARATION
        
    return BehaviourStage.AWARENESS