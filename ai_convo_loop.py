from gpt import get_ai_response
from elevenlabs import text_to_speech
from config import LIVE_TRANSFER_NUMBER

handoff_keywords = ["yes", "need funding", "cash advance", "monthly revenue", "$"]

def get_ai_response_and_audio(transcript):
    response_text = get_ai_response(transcript)
    print(f"[AI]: {response_text}")
    if any(keyword in transcript.lower() for keyword in handoff_keywords):
        print("Triggering live transfer...")
        response_text += " One moment while I connect you to a funding specialist..."
        # This is where a live transfer would be triggered in the backend
    audio = text_to_speech(response_text)
    return audio