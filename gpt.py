import openai
from config import OPENAI_API_KEY

openai.api_key = OPENAI_API_KEY
openai.organization = "org-vGU6JoNgNsNnPbmv0mhXUINT"  # ✅ Added your org ID

def get_ai_response(prompt):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "You're a friendly funding assistant calling small business owners."},
                {"role": "user", "content": prompt}
            ],
            timeout=10
        )
        return response['choices'][0]['message']['content']
    except Exception as e:
        print("❌ GPT Error:", e)
        return "Sorry, I had trouble understanding that. Can you repeat?"
