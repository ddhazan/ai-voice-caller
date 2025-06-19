from gpt import get_ai_response
from elevenlabs import text_to_speech

def get_ai_response_and_audio(transcript):
    response_text = get_ai_response(transcript)
    audio = text_to_speech(response_text)
    return audio