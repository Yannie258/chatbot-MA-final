import os
import json
from openai import OpenAI
from models.schemas import ChatResponse
from langchain.vectorstores import FAISS
from langchain.embeddings import OpenAIEmbeddings

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def generate_response(user_message: str, strategy="plain") -> ChatResponse:
    content_type = "text"
    messages = []
    tools = None
    tool_choice = None

    # Add RAG context for all strategies
    embeddings = OpenAIEmbeddings(openai_api_key=os.getenv("OPENAI_API_KEY"))
    db = FAISS.load_local("vector_index", embeddings, allow_dangerous_deserialization=True)
    docs = db.similarity_search(user_message, k=3)
    context = "\n".join([doc.page_content for doc in docs])

    if strategy == "plain":
        # Plain text → no JSON parsing
        prompt = f"""
        You are a helpful student onboarding assistant at TU Chemnitz.
        Answer the following question in **plain natural text** only.

        Use the following context to answer:
        {context}

        Style rules:
        - Be **clear and concise**, avoid long academic paragraphs.
        - Use a friendly intro sentence.
        - For each important item, start with a **short bold headline** (intent).
        - Place details in a **new line** under that headline, not in the same line.
        - Use bullet points (•) for lists.
        - Add blank lines between items for readability.
        - Keep the tone warm and encouraging.
        - End with a follow-up suggestion to keep the conversation going.

        Question: {user_message}
        """
        content_type = "text"
        messages = [
            {"role": "system", "content": "You are a helpful student onboarding assistant at TU Chemnitz."},
            {"role": "user", "content": prompt}
        ]

    elif strategy == "icl":
        # One-shot ICL example
        prompt = f"""
        You are a helpful student onboarding assistant at TU Chemnitz.
        Always answer in JSON format with this schema:
        {{
          "type": "card",
          "title": "string",
          "description": "string",
          "action_url": "string",
          "action_label": "string"
        }}

        Use the following context to answer:
        {context}

        Example:
        Q: Where can I find the cafeteria?
        A:
        {{
          "type": "card",
          "title": "Mensa (Cafeteria)",
          "description": "The main Mensa is located on Reichenhainer Straße. You can get affordable meals here during weekdays.",
          "action_url": "https://www.swcz.de/mensen-cafeterien/mensen-und-cafeterien-in-chemnitz/",
          "action_label": "View Menu"
        }}

        Now answer the user's question in the same JSON format.

        Q: {user_message}
        """
        content_type = "card"
        messages = [
            {"role": "system", "content": "You are a helpful student onboarding assistant at TU Chemnitz."},
            {"role": "user", "content": prompt}
        ]

    elif strategy == "cot":
        # CoT reasoning
        prompt = f"""
        You are a helpful student onboarding assistant at TU Chemnitz.

        Use ONLY the URLs and facts from the provided context:
        {context}

        If no URL is available in the context, leave the "action_url" field empty. 
        Replace any url starting with https://www.stadt-chemnitz.de with https://www.chemnitz.de

        Follow these steps:
        1. First, think step by step about the answer (this reasoning is hidden).
        2. Then, output only the final structured answer in JSON format with this schema:
        {{
          "type": "card",
          "title": "string",
          "description": "string",
          "action_url": "string",
          "action_label": "string"
        }}

        Question: {user_message}

        Final Answer (JSON only):
        """
        content_type = "card"
        messages = [
            {"role": "system", "content": "You are a helpful student onboarding assistant at TU Chemnitz."},
            {"role": "user", "content": prompt}
        ]

    elif strategy == "function":
        # Define schema for card output
        tools = [
            {
                "type": "function",
                "function": {
                    "name": "create_card",
                    "description": "Generate a structured card with onboarding information",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "type": {"type": "string", "enum": ["card"]},
                            "title": {"type": "string"},
                            "description": {"type": "string"},
                            "action_url": {"type": "string"},
                            "action_label": {"type": "string"}
                        },
                        "required": ["type", "title", "description", "action_label"]
                    }
                }
            }
        ]
        tool_choice = {"type": "function", "function": {"name": "create_card"}}
        content_type = "card"
        
        # For function calling, use a simpler prompt
        messages = [
            {"role": "system", "content": "You are a helpful student onboarding assistant at TU Chemnitz. Use the provided context to answer questions."},
            {"role": "user", "content": f"Context: {context}\n\nQuestion: {user_message}"}
        ]

    else:
        raise ValueError(f"Unknown strategy: {strategy}")

    # Call OpenAI API
    if strategy == "function":
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=messages,
            tools=tools,
            tool_choice=tool_choice,
            temperature=0.2
        )
        
        # Extract function call arguments
        tool_calls = response.choices[0].message.tool_calls
        if tool_calls:
            raw_output = tool_calls[0].function.arguments
            try:
                parsed_output = json.loads(raw_output)
            except json.JSONDecodeError as e:
                parsed_output = {"error": "Invalid JSON", "raw": raw_output, "details": str(e)}
        else:
            # Fallback if no function call is made
            content = response.choices[0].message.content
            parsed_output = {"error": "No function call made", "raw_response": content}
            
    else:
        # For non-function strategies
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=messages,
            temperature=0.2
        )
        
        content = response.choices[0].message.content
        
        if strategy == "plain":
            parsed_output = content
        else:
            # Try to parse JSON for ICL and CoT strategies
            try:
                parsed_output = json.loads(content)
            except json.JSONDecodeError as e:
                parsed_output = {"error": "Invalid JSON", "raw": content, "details": str(e)}

    return ChatResponse(role="bot", content_type=content_type, content=parsed_output)