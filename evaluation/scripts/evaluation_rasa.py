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
# Query Rasa
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
# Entity comparison
# --------------------------------------------------

def normalize_entity(entity):
    return (
        entity.get("entity", "").strip().lower(),
        entity.get("value", "").strip().lower()
    )


def compare_entities(expected, predicted):

    expected_set = {
        normalize_entity(entity)
        for entity in expected
    }

    predicted_set = {
        normalize_entity(entity)
        for entity in predicted
    }

    true_positives = len(
        expected_set & predicted_set
    )

    false_positives = len(
        predicted_set - expected_set
    )

    false_negatives = len(
        expected_set - predicted_set
    )

    return (
        true_positives,
        false_positives,
        false_negatives
    )


# --------------------------------------------------
# Main evaluation
# --------------------------------------------------

def main():

    print("=" * 60)
    print("AarogyaMitra - Rasa Evaluation")
    print("=" * 60)

    questions = load_questions()

    results = []

    correct_intents = 0

    total_tp = 0
    total_fp = 0
    total_fn = 0

    for question in questions:

        question_id = question["id"]
        text = question["text"]

        expected_intent = question["expected_intent"]
        expected_entities = question.get(
            "expected_entities", []
        )

        print(f"\nQuestion {question_id}")
        print(f"Text: {text}")

        try:

            data = query_rasa(text)

            # --------------------------------------
            # Intent evaluation
            # --------------------------------------

            intent_data = data.get("intent", {})

            predicted_intent = intent_data.get("name")
            intent_confidence = intent_data.get(
                "confidence", 0.0
            )

            intent_correct = (
                predicted_intent == expected_intent
            )

            if intent_correct:
                correct_intents += 1

            # --------------------------------------
            # Entity evaluation
            # --------------------------------------

            predicted_entities = data.get(
                "entities", []
            )

            tp, fp, fn = compare_entities(
                expected_entities,
                predicted_entities
            )

            total_tp += tp
            total_fp += fp
            total_fn += fn

            entity_correct = (
                tp == len(expected_entities)
                and fp == 0
            )

            # --------------------------------------
            # Display
            # --------------------------------------

            print(
                f"Expected intent : {expected_intent}"
            )

            print(
                f"Predicted intent: {predicted_intent}"
            )

            print(
                f"Confidence      : "
                f"{intent_confidence:.4f}"
            )

            print(
                f"Expected entities: "
                f"{expected_entities}"
            )

            print(
                f"Predicted entities: "
                f"{predicted_entities}"
            )

            print(
                f"Entity TP={tp}, FP={fp}, FN={fn}"
            )

            print(
                "Intent result   : "
                + ("PASS" if intent_correct else "FAIL")
            )

            print(
                "Entity result   : "
                + ("PASS" if entity_correct else "FAIL")
            )

            # --------------------------------------
            # Store result
            # --------------------------------------

            results.append({
                "id": question_id,
                "text": text,
                "expected_intent": expected_intent,
                "predicted_intent": predicted_intent,
                "intent_confidence": intent_confidence,
                "intent_correct": intent_correct,
                "expected_entities": expected_entities,
                "predicted_entities": predicted_entities,
                "entity_true_positive": tp,
                "entity_false_positive": fp,
                "entity_false_negative": fn,
                "entity_correct": entity_correct
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
                "expected_entities": expected_entities,
                "predicted_entities": [],
                "entity_true_positive": 0,
                "entity_false_positive": 0,
                "entity_false_negative": len(
                    expected_entities
                ),
                "entity_correct": False,
                "error": str(error)
            })

            total_fn += len(expected_entities)

    # --------------------------------------------------
    # Intent accuracy
    # --------------------------------------------------

    total_questions = len(questions)

    intent_accuracy = (
        correct_intents / total_questions
        if total_questions
        else 0.0
    )

    # --------------------------------------------------
    # Entity precision / recall / F1
    # --------------------------------------------------

    if total_tp + total_fp > 0:
        entity_precision = (
            total_tp /
            (total_tp + total_fp)
        )
    else:
        entity_precision = 0.0

    if total_tp + total_fn > 0:
        entity_recall = (
            total_tp /
            (total_tp + total_fn)
        )
    else:
        entity_recall = 0.0

    if entity_precision + entity_recall > 0:
        entity_f1 = (
            2 *
            entity_precision *
            entity_recall /
            (entity_precision + entity_recall)
        )
    else:
        entity_f1 = 0.0

    # --------------------------------------------------
    # Create report
    # --------------------------------------------------

    report = {

        "total_questions": total_questions,

        "intent_evaluation": {
            "correct": correct_intents,
            "incorrect": (
                total_questions -
                correct_intents
            ),
            "accuracy": round(
                intent_accuracy * 100,
                2
            )
        },

        "entity_evaluation": {
            "true_positives": total_tp,
            "false_positives": total_fp,
            "false_negatives": total_fn,
            "precision": round(
                entity_precision * 100,
                2
            ),
            "recall": round(
                entity_recall * 100,
                2
            ),
            "f1_score": round(
                entity_f1 * 100,
                2
            )
        },

        "results": results
    }

    # --------------------------------------------------
    # Save report
    # --------------------------------------------------

    RESULTS_DIR.mkdir(
        parents=True,
        exist_ok=True
    )

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
        f"Intent accuracy : "
        f"{intent_accuracy * 100:.2f}%"
    )

    print(
        f"Entity precision: "
        f"{entity_precision * 100:.2f}%"
    )

    print(
        f"Entity recall   : "
        f"{entity_recall * 100:.2f}%"
    )

    print(
        f"Entity F1       : "
        f"{entity_f1 * 100:.2f}%"
    )

    print("=" * 60)

    print("\nResults saved to:")
    print(OUTPUT_FILE)


if __name__ == "__main__":
    main()