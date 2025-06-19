# AI Voice Caller Backend (Python)

## Features
- Outbound call using Twilio
- AI voice response using OpenAI GPT-4o + ElevenLabs
- Seamless transfer to real human

## Environment Variables
Set these on Render or locally:

```
TWILIO_ACCOUNT_SID=
TWILIO_AUTH_TOKEN=
TWILIO_PHONE_NUMBER=
ELEVENLABS_API_KEY=
OPENAI_API_KEY=
LIVE_TRANSFER_NUMBER=
```

## Start Locally
```bash
pip install -r requirements.txt
python app.py
```

## Deploy on Render
- Build Command: `pip install -r requirements.txt`
- Start Command: `gunicorn app:app`