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
    print("📞 Call initiated to", to_number, "SID:", sid)
    return {"message": "Call initiated", "sid": sid}

@app.websocket("/media")
async def media_stream(websocket: WebSocket):
    await websocket.accept()
    print("🎙 WebSocket connection accepted")

    # Immediately send intro audio to keep call alive and simulate greeting
    greeting_audio = get_ai_response_and_audio("Hi, this is Dan from Thermal Capital. I just have a few quick questions.")
    base64_audio = base64.b64encode(greeting_audio).decode("utf-8")
    await websocket.send_json({
        "event": "media",
        "media": {"payload": base64_audio}
    })

    try:
        while True:
            message = await websocket.receive_bytes()
            print("📥 Received audio bytes:", len(message))

            # Replace with Deepgram transcript in future
            prompt = "I'm checking to see if your business accepts card payments and might benefit from funding."

            response_audio = get_ai_response_and_audio(prompt)
            print("📤 Sending audio payload:", len(response_audio))

            base64_audio = base64.b64encode(response_audio).decode("utf-8")
            await websocket.send_json({
                "event": "media",
                "media": {"payload": base64_audio}
            })

    except Exception as e:
        print("❌ WebSocket closed or failed:", str(e))