from twilio.rest import Client
from config import TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN, TWILIO_PHONE_NUMBER

client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

def initiate_call(to_number):
    twiml = f"""
    <Response>
        <Start>
            <Stream url="wss://ai-voice-caller-gc38.onrender.com/media" />
        </Start>
        <Say voice='Polly.Joanna'>Hi, this is Dan from Thermal Capital. I just have a couple quick questions...</Say>
    </Response>
    """
    call = client.calls.create(
        twiml=twiml,
        to=to_number,
        from_=TWILIO_PHONE_NUMBER
    )
    return call.sid
