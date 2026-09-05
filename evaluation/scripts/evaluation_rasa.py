import json
from pathlib import Path

import requests


# --------------------------------------------------
# Paths
# --------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent.parent

QUESTIONS_FILE = BASE_DIR / "dataset" / "rasa_questions.json"
RESULTS_DIR = BASE_DIR / "results"
OUTPUT_FILE = RESULTS_DIR / "rasa_results.json"


# --------------------------------------------------
# Rasa API
# --------------------------------------------------

RASA_URL = "http://127.0.0.1:5005/model/parse"


# --------------------------------------------------
# Load questions
# --------------------------------------------------

def load_questions():
    with open(QUESTIONS_FILE, "r", encoding="utf-8") as file:
        return json.load(file)


# --------------------------------------------------
# Send question to Rasa
# --------------------------------------------------

def query_rasa(text):
    response = requests.post(
        RASA_URL,
        json={"text": text},
        timeout=30
    )

    response.raise_for_status()

    return response.json()


# --------------------------------------------------
# Evaluate
# --------------------------------------------------

def main():

    print("=" * 60)
    print("AarogyaMitra - Rasa Evaluation")
    print("=" * 60)

    questions = load_questions()

    results = []

    correct_intents = 0
    correct_entities = 0
    entity_tests = 0

    for question in questions:

        question_id = question["id"]
        text = question["text"]
        expected_intent = question["expected_intent"]

        print(f"\nQuestion {question_id}")
        print(f"Text: {text}")

        try:
            data = query_rasa(text)

            # ------------------------------
            # Intent
            # ------------------------------

            intent_data = data.get("intent", {})

            predicted_intent = intent_data.get("name")
            intent_confidence = intent_data.get("confidence", 0.0)

            intent_correct = (
                predicted_intent == expected_intent
            )

            if intent_correct:
                correct_intents += 1

            # ------------------------------
            # Entities
            # ------------------------------

            predicted_entities = data.get("entities", [])

            entity_result = []

            for entity in predicted_entities:

                entity_result.append({
                    "entity": entity.get("entity"),
                    "value": entity.get("value"),
                    "confidence": entity.get(
                        "confidence_entity", 0.0
                    )
                })

            # ------------------------------
            # Print result
            # ------------------------------

            print(f"Expected intent : {expected_intent}")
            print(f"Predicted intent: {predicted_intent}")
            print(f"Confidence      : {intent_confidence:.4f}")

            if intent_correct:
                print("Intent result   : PASS")
            else:
                print("Intent result   : FAIL")

            if entity_result:
                print(f"Entities        : {entity_result}")

            # ------------------------------
            # Store result
            # ------------------------------

            results.append({
                "id": question_id,
                "text": text,
                "expected_intent": expected_intent,
                "predicted_intent": predicted_intent,
                "intent_confidence": intent_confidence,
                "intent_correct": intent_correct,
                "entities": entity_result
            })

        except requests.exceptions.RequestException as error:

            print("ERROR: Could not connect to Rasa.")
            print(error)

            results.append({
                "id": question_id,
                "text": text,
                "expected_intent": expected_intent,
                "predicted_intent": None,
                "intent_confidence": None,
                "intent_correct": False,
                "entities": [],
                "error": str(error)
            })

    # --------------------------------------------------
    # Calculate accuracy
    # --------------------------------------------------

    total_questions = len(questions)

    intent_accuracy = (
        correct_intents / total_questions * 100
        if total_questions
        else 0
    )

    # --------------------------------------------------
    # Save results
    # --------------------------------------------------

    RESULTS_DIR.mkdir(
        parents=True,
        exist_ok=True
    )

    report = {
        "total_questions": total_questions,
        "correct_intents": correct_intents,
        "incorrect_intents": (
            total_questions - correct_intents
        ),
        "intent_accuracy_percent": round(
            intent_accuracy, 2
        ),
        "results": results
    }

    with open(
        OUTPUT_FILE,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            report,
            file,
            indent=2,
            ensure_ascii=False
        )

    # --------------------------------------------------
    # Final summary
    # --------------------------------------------------

    print("\n" + "=" * 60)
    print("RASA EVALUATION SUMMARY")
    print("=" * 60)

    print(
        f"Total questions : {total_questions}"
    )

    print(
        f"Correct intents : {correct_intents}"
    )

    print(
        f"Intent accuracy : {intent_accuracy:.2f}%"
    )

    print("=" * 60)

    print("\nResults saved to:")
    print(OUTPUT_FILE)


if __name__ == "__main__":
    main()