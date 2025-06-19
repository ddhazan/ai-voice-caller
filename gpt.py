import openai
from config import OPENAI_API_KEY

openai.api_key = OPENAI_API_KEY
openai.organization = "org-vGU6JoNgNsNnPbmv0mhXUINT"

def get_ai_response(prompt):
    print("🔁 GPT prompt received:", prompt)
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "You're a friendly funding assistant calling small business owners."},
                {"role": "user", "content": prompt}
            ],
            timeout=10
        )
        answer = response['choices'][0]['message']['content']
        print("✅ GPT response:", answer)
        return answer
    except Exception as e:
        print("❌ GPT error:", e)
        return "Sorry, something went wrong."
