import openai
import os
from models.schemas import ChatResponse

openai.api_key = os.getenv("OPENAI_API_KEY")

def generate_response(user_message: str) -> ChatResponse:
    prompt = f"""
You are a helpful chatbot. Respond in this JSON format:

{{
  "content_type": "card",
  "content": {{
    "title": "Answer",
    "body": "Response to the user.",
    "actions": ["More Info", "Help"]
  }}
}}

User question: {user_message}
"""

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.2,
    )

    return ChatResponse(
        role="bot",
        content_type="text",  # For now, return raw text (can parse later)
        content=response['choices'][0]['message']['content']
    )
