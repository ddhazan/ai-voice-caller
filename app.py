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