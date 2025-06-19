import openai
from config import OPENAI_API_KEY

openai.api_key = OPENAI_API_KEY

def get_ai_response(prompt):
    response = openai.ChatCompletion.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "You're a friendly funding assistant calling small business owners."},
            {"role": "user", "content": prompt}
        ]
    )
    return response['choices'][0]['message']['content']