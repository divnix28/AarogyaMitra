from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
import json
import logging

logger = logging.getLogger(__name__)

class ActionRouteNLUPayload(Action):
    def name(self) -> Text:
        return "action_route_nlu_payload"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any]
    ) -> List[Dict[Text, Any]]:

        latest_message = tracker.latest_message
        
        intent = latest_message.get("intent", {})
        intent_name = intent.get("name", "nlu_fallback")
        intent_confidence = intent.get("confidence", 0.0)
        
        raw_entities = latest_message.get("entities", [])
        
        parsed_entities = []
        for ent in raw_entities:
            parsed_entities.append({
                "entity": ent.get("entity"),
                "value": ent.get("value"),
                "confidence": ent.get("confidence_entity", 1.0),
                "start": ent.get("start"),
                "end": ent.get("end")
            })

        payload = {
            "text": tracker.latest_message.get("text", ""),
            "intent": {
                "name": intent_name,
                "confidence": round(intent_confidence, 4)
            },
            "entities": parsed_entities,
            "slots": {
                "disease": tracker.get_slot("disease"),
                "symptom": tracker.get_slot("symptom"),
                "vaccine": tracker.get_slot("vaccine")
            },
            "is_emergency": intent_name == "emergency"
        }

        logger.info(f"Rasa Action Output Payload: {json.dumps(payload)}")
        dispatcher.utter_message(json_message=payload)

        return []


class ActionHandleEmergency(Action):
    def name(self) -> Text:
        return "action_handle_emergency"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any]
    ) -> List[Dict[Text, Any]]:

        emergency_payload = {
            "text": tracker.latest_message.get("text", ""),
            "intent": {
                "name": "emergency",
                "confidence": 1.0
            },
            "entities": tracker.latest_message.get("entities", []),
            "is_emergency": True,
            "escalation_required": True,
            "emergency_contacts": ["108", "102"]
        }

        dispatcher.utter_message(response="utter_emergency_escalation")
        dispatcher.utter_message(json_message=emergency_payload)

        return []