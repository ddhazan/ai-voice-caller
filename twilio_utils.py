from twilio.rest import Client
from config import TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN, TWILIO_PHONE_NUMBER, LIVE_TRANSFER_NUMBER

client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

def initiate_call(to_number):
    twiml = f"""
    <Response>
        <Say voice='Polly.Joanna'>Hi, this is Dan from Thermal Capital. One moment...</Say>
        <Dial>{LIVE_TRANSFER_NUMBER}</Dial>
    </Response>
    """
    call = client.calls.create(
        twiml=twiml,
        to=to_number,
        from_=TWILIO_PHONE_NUMBER
    )
    return call.sid