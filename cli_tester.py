import json

from backend.app.safety.safety_validator import check_hard_override
from backend.app.hrrs.calculator import calculate_hrrs_score
from backend.app.learning.teachback import evaluate_misconception
def run_safety_suite():
    print("\n--- Running Safety Override Tests ---")
    cases = ["Severe chest pain radiating to jaw", "Mild headache"]
    for case in cases:
        try:
            print(f"Test: {case}\nResult: {check_hard_override(case)}\n")
        except Exception as e:
            print(f"Error handling query: {e}")

def run_hrrs_suite():
    print("\n--- Running HRRS Threshold Tests ---")
    cases = [
        {"symptoms": ["mild headache"], "confidence": 0.85},
        {"symptoms": ["fever", "fatigue", "night sweats"], "confidence": 0.45},
        {"symptoms": [], "confidence": 0.99}
    ]
    for c in cases:
        try:
            result = calculate_hrrs_score(c['symptoms'], c['confidence'])
            print(f"Test: {c['symptoms']} | AI Score: {c['confidence']}\nOutput: {result}\n")
        except Exception as e:
            print(f"Error processing list: {e}")

def run_teachback_suite():
    print("\n--- Running Teach-Back Loop Tests ---")
    try:
        result = evaluate_misconception("Take for 5 days", "Take until fever stops")
        print(f"Test: Antibiotic timeline\nOutput: {result}\n")
    except Exception as e:
        print(f"Error evaluating text: {e}")

def main_menu():
    while True:
        print("\n=== AarogyaMitra Member 5 CLI Harness ===")
        choice = input("1. Safety | 2. HRRS | 3. Teach-Back | 4. Exit\nSelect (1-4): ")
        
        if choice == '1': run_safety_suite()
        elif choice == '2': run_hrrs_suite()
        elif choice == '3': run_teachback_suite()
        elif choice == '4': break
        else: print("Invalid selection.")

if __name__ == "__main__":
    main_menu()