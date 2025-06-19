from fastapi import FastAPI, WebSocket, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from twilio_utils import initiate_call
from ai_logic import get_ai_response_and_audio
import base64
import json

app = FastAPI()

# ✅ Allow Twilio preflight and headers
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
@app.api_route("/", methods=["GET", "HEAD"])
def root():
    return {"status": "ok"}

# ✅ Twilio may send a HEAD or GET to check if /media exists
@app.get("/media")
def media_health_check():
    return {"status": "OK"}

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

    try:
        # Send initial ElevenLabs voice greeting
        greeting_text = "Hi, this is Dan from Thermal Capital. I just have a few quick questions."
        greeting_audio = get_ai_response_and_audio(greeting_text)
        base64_audio = base64.b64encode(greeting_audio).decode("utf-8")

        await websocket.send_text(json.dumps({
            "event": "media",
            "media": {"payload": base64_audio}
        }))
        print("✅ Sent greeting audio")

        while True:
            message = await websocket.receive_bytes()
            print("📥 Received audio chunk:", len(message))

            # Placeholder for real speech-to-text
            prompt = "Do you currently accept credit card payments from customers?"

            response_audio = get_ai_response_and_audio(prompt)
            base64_audio = base64.b64encode(response_audio).decode("utf-8")

            await websocket.send_text(json.dumps({
                "event": "media",
                "media": {"payload": base64_audio}
            }))
            print("📤 Sent AI response audio")

    except Exception as e:
        print("❌ WebSocket error:", str(e))
