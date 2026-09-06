from enum import Enum

class HRRSAction(str, Enum):
    ANSWER = "ANSWER"
    ANSWER_PREVENTIVE = "ANSWER_PREVENTIVE"
    ASK_MORE = "ASK_MORE"
    ASHA_REFERRAL = "ASHA_REFERRAL"
    ESCALATE = "ESCALATE"

def determine_action(score: float) -> HRRSAction:
    if score >= 90.0:
        return HRRSAction.ANSWER
    elif score >= 75.0:
        return HRRSAction.ANSWER_PREVENTIVE
    elif score >= 60.0:
        return HRRSAction.ASK_MORE
    elif score >= 40.0:
        return HRRSAction.ASHA_REFERRAL
    else:
        return HRRSAction.ESCALATE