import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def generate_response(messages):
    """
    Calls Groq LLM and returns text output.
    `messages` must be a list of dicts: [{"role": ..., "content": ...}]
    """
    try:
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=messages,
            temperature=0.7,
            max_tokens=1024,
        )
        return response.choices[0].message.content.strip()

    except Exception as e:
        return f"⚠️ Error: {str(e)}"
