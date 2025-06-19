from flask import Flask, request, jsonify
from config import TWILIO_PHONE_NUMBER, LIVE_TRANSFER_NUMBER
from twilio_utils import initiate_call
import os

app = Flask(__name__)

@app.route("/")
def home():
    return "AI Voice Caller Backend is running."

@app.route("/call", methods=["POST"])
def call():
    data = request.json
    to_number = data.get("to")
    if not to_number:
        return jsonify({"error": "Missing 'to' number."}), 400
    call_sid = initiate_call(to_number)
    return jsonify({"message": "Call initiated", "sid": call_sid})
    from media_stream import stream_handler
import asyncio
import websockets
from flask import Response

@app.route("/media")
def media_route():
    return Response("WebSocket only", 400)

def start_websocket():
    return websockets.serve(stream_handler, "0.0.0.0", 10000)

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(start_websocket())
    app.run(host="0.0.0.0", port=10000)
