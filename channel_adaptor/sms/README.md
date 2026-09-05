# SMS Channel Adapter

This module handles communication between AarogyaMitra and SMS.

## Components

### webhook.py

Receives incoming SMS messages and converts them into the common AarogyaMitra message format.

### formatter.py

Formats AI responses for SMS.

### sender.py

Sends responses through the configured SMS provider.

## Message Flow

SMS User
→ SMS Provider
→ webhook.py
→ CommonMessage
→ AarogyaMitra AI
→ formatter.py
→ sender.py
→ SMS User

## API Configuration

The SMS provider will be configured later.

Required values:

- SMS API URL
- SMS API Key
- SMS Sender ID