import requests
import io
from pydub import AudioSegment

from config import ELEVENLABS_API_KEY, ELEVENLABS_VOICE_ID

def get_ai_response_and_audio(text):
    response = requests.post(
        f"https://api.elevenlabs.io/v1/text-to-speech/{ELEVENLABS_VOICE_ID}",
        headers={
            "xi-api-key": ELEVENLABS_API_KEY,
            "Accept": "audio/pcm",
            "Content-Type": "application/json"
        },
        json={
            "text": text,
            "model_id": "eleven_monolingual_v1"
        }
    )

    if response.status_code != 200:
        raise Exception(f"ElevenLabs error: {response.status_code} - {response.text}")

    # Convert raw PCM to 8kHz mono μ-law for Twilio
    raw_audio = io.BytesIO(response.content)
    audio = AudioSegment.from_file(
        raw_audio,
        format="raw",
        frame_rate=22050,
        channels=1,
        sample_width=2
    )
    ulaw = audio.set_frame_rate(8000).set_channels(1).set_sample_width(1)

    out = io.BytesIO()
    ulaw.export(out, format="ulaw")
    return out.read()