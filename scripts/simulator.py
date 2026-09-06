import requests
import datetime
import json

API_URL = "http://127.0.0.1:8000/api/v1/chat/message"

def send_message(message_text, channel="whatsapp", user_id="local_tester_01"):
    payload = {
        "channel": channel,
        "user_id": user_id,
        "message": message_text,
        "language": "en",
        "timestamp": datetime.datetime.now(datetime.timezone.utc).isoformat()
    }
    
    try:
        response = requests.post(API_URL, json=payload)
        data = response.json()
        print(f"\n[{channel.upper()} USER] {message_text}")
        print(f"[AAROGYAMITRA] {data.get('message')}")
        print(f"[METADATA] Action: {data.get('action')} | Intent: {data.get('intent')}\n")
    except requests.exceptions.ConnectionError:
        print("\n[ERROR] Backend is unreachable. Is Uvicorn running on port 8000?\n")

if __name__ == "__main__":
    print("=== AarogyaMitra Local Simulator ===")
    print("Type your message and press Enter (Type 'quit' to exit)")
    
    while True:
        user_input = input("> ")
        if user_input.lower() in ['quit', 'exit']:
            break
        send_message(user_input)
