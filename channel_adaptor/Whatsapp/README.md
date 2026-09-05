# WhatsApp Channel Adapter

This module handles communication between AarogyaMitra and WhatsApp.

## Components

### webhook.py

Receives incoming WhatsApp messages and converts them into the common AarogyaMitra message format.

### formatter.py

Formats AI responses for WhatsApp.

### sender.py

Sends responses through the WhatsApp API.

## Message Flow

WhatsApp User
→ WhatsApp API
→ webhook.py
→ CommonMessage
→ AarogyaMitra AI
→ formatter.py
→ sender.py
→ WhatsApp User

## API Configuration

The WhatsApp API credentials will be configured later.

Required values:

- WhatsApp Access Token
- WhatsApp Phone Number ID
- Graph API URL