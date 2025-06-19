from fastapi import FastAPI, WebSocket, Request
from fastapi.responses import JSONResponse
from twilio_utils import initiate_call
from ai_logic import get_ai_response_and_audio
import base64

app = FastAPI()

@app.post("/call")
async def call_endpoint(request: Request):
    data = await request.json()
    to_number = data.get("to")
    if not to_number:
        return JSONResponse({"error": "Missing 'to' number."}, status_code=400)
    sid = initiate_call(to_number)
    return {"message": "Call initiated", "sid": sid}

@app.websocket("/media")
async def media_stream(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            message = await websocket.receive_bytes()
            audio_bytes = get_ai_response_and_audio("I'm just getting started.")  # placeholder
            base64_audio = base64.b64encode(audio_bytes).decode("utf-8")
            await websocket.send_json({
                "event": "media",
                "media": {"payload": base64_audio}
            })
    except Exception as e:
        print("WebSocket closed or failed:", str(e))