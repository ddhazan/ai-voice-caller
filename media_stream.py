import asyncio
import websockets
import json
import base64
from deepgram import Deepgram
from config import DEEPGRAM_API_KEY
from ai_convo_loop import get_ai_response_and_audio

dg_client = Deepgram(DEEPGRAM_API_KEY)

async def stream_handler(websocket, path):
    print("WebSocket connection started")
    dg_connection = await dg_client.transcription.live({
        'punctuate': True,
        'interim_results': False
    })
    await dg_connection.start()

    async def handle_transcription():
        async for msg in dg_connection:
            transcript = msg.get('channel', {}).get('alternatives', [{}])[0].get('transcript', '')
            if transcript:
                print(f"[User]: {transcript}")
                audio_bytes = get_ai_response_and_audio(transcript)
                # Encode audio as base64 and send as Twilio-compatible message
                base64_audio = base64.b64encode(audio_bytes).decode("utf-8")
                twilio_msg = json.dumps({
                    "event": "media",
                    "media": {
                        "payload": base64_audio
                    }
                })
                await websocket.send(twilio_msg)

    asyncio.create_task(handle_transcription())

    try:
        async for message in websocket:
            if isinstance(message, bytes):
                await dg_connection.send(message)
    except websockets.exceptions.ConnectionClosedOK:
        print("WebSocket connection closed")
    finally:
        await dg_connection.finish()
