import asyncio
import websockets
import json
from deepgram import Deepgram
from config import DEEPGRAM_API_KEY
from ai_convo_loop import get_ai_response_and_audio

dg_client = Deepgram(DEEPGRAM_API_KEY)

sessions = {}

async def stream_handler(websocket, path):
    session_id = id(websocket)
    print(f"New session {session_id} started.")
    dg_connection = await dg_client.transcription.live({'punctuate': True, 'interim_results': False})
    await dg_connection.start()

    async def process_transcripts():
        async for msg in dg_connection:
            transcript = msg.get('channel', {}).get('alternatives', [{}])[0].get('transcript', '')
            if transcript:
                print(f"[User]: {transcript}")
                audio = get_ai_response_and_audio(transcript)
                await websocket.send(audio)

    asyncio.create_task(process_transcripts())

    try:
        async for message in websocket:
            if isinstance(message, bytes):
                await dg_connection.send(message)
    except websockets.exceptions.ConnectionClosedOK:
        print(f"Session {session_id} closed.")
    finally:
        await dg_connection.finish()