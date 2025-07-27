import os
from openai import OpenAI
from models.schemas import ChatResponse

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def generate_response(user_message: str) -> ChatResponse:
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": user_message}],
        temperature=0.2
    )

    return ChatResponse(
        role="bot",
        content_type="text",
        content=response.choices[0].message.content
    )
