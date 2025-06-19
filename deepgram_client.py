from deepgram import Deepgram
from config import DEEPGRAM_API_KEY

dg_client = Deepgram(DEEPGRAM_API_KEY)

async def transcribe_audio_stream(audio_generator):
    response = await dg_client.transcription.prerecorded(
        audio_generator,
        {'punctuate': True}
    )
    return response['results']['channels'][0]['alternatives'][0]['transcript']
