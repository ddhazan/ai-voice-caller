import requests
import io
import base64
from elevenlabs import generate
from pydub import AudioSegment

from config import ELEVENLABS_API_KEY, ELEVENLABS_VOICE_ID

def get_ai_response_and_audio(text):
    # Generate audio from ElevenLabs (MP3 format)
    audio_stream = generate(
        text=text,
        voice=ELEVENLABS_VOICE_ID,
        model="eleven_monolingual_v1",
        api_key=ELEVENLABS_API_KEY
    )

    # Convert streamed audio into bytes
    audio_bytes = io.BytesIO()
    for chunk in audio_stream:
        audio_bytes.write(chunk)
    audio_bytes.seek(0)

    # Convert to 8kHz mono mulaw using pydub
    audio = AudioSegment.from_file(audio_bytes, format="mp3")
    ulaw_audio = audio.set_frame_rate(8000).set_channels(1).set_sample_width(1)

    out_buffer = io.BytesIO()
    ulaw_audio.export(out_buffer, format="ulaw")
    out_buffer.seek(0)

    return out_buffer.read()