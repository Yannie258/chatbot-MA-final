# backend/app/services/rag.py
import os
from openai import OpenAI
from models.schemas import ChatResponse
from langchain.vectorstores import FAISS
from langchain.embeddings import OpenAIEmbeddings

class RAGService:
    def __init__(self, index_path="vector_index"):
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        embeddings = OpenAIEmbeddings(openai_api_key=os.getenv("OPENAI_API_KEY"))
        self.db = FAISS.load_local(index_path, embeddings, allow_dangerous_deserialization=True)

    def _retrieve_context(self, query: str, k: int = 3) -> str:
        docs = self.db.similarity_search(query, k=k)
        return "\n".join([doc.page_content for doc in docs])

    def generate_response(self, user_message: str, strategy="plain", model="gpt-4o-mini", temperature=0.2) -> ChatResponse:
        context = self._retrieve_context(user_message)

        if strategy == "plain":
            return self._generate_plain(user_message, context, model, temperature)
        elif strategy == "structured":
            return self._generate_structured(user_message, context, model, temperature)
        else:
            raise ValueError(f"Unknown strategy: {strategy}")

    def _generate_plain(self, user_message, context, model, temperature):
        prompt = f"""
        You are a helpful student onboarding assistant at TU Chemnitz.
        Use the following context to answer:
        {context}

        Answer in **plain natural text** only.
        - Clear and concise
        - Bold headlines
        - Bullet points for lists
        - End with a follow-up suggestion

        Question: {user_message}
        """

        response = self.client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": prompt}],
            temperature=temperature
        )

        return ChatResponse(
            role="bot",
            content_type="text",
            content=response.choices[0].message.content
        )

    def _generate_structured(self, user_message, context, model, temperature):
        # Define function schema (OpenAI "tools")
        tools = [
            {
                "type": "function",
                "function": {
                    "name": "create_card",
                    "description": "Return structured output aligned with GUI",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "type": {"type": "string", "enum": ["card", "list", "quick_reply"]},
                            "title": {"type": "string"},
                            "body": {"type": "string"},
                            "actions": {
                                "type": "array",
                                "items": {
                                    "type": "object",
                                    "properties": {
                                        "label": {"type": "string"},
                                        "url": {"type": "string"}
                                    },
                                    "required": ["label", "url"]
                                }
                            }
                        },
                        "required": ["type", "title", "body"]
                    }
                }
            }
        ]

        response = self.client.chat.completions.create(
            model=model,
            temperature=temperature,
            messages=[
                {"role": "system", "content": "You are a TU Chemnitz onboarding assistant. Always call create_card."},
                {"role": "user", "content": f"Context:\n{context}\n\nQuestion: {user_message}"}
            ],
            tools=tools,
            tool_choice={"type": "function", "function": {"name": "create_card"}}
        )

        # Extract structured output from tool call
        tool_call = response.choices[0].message.tool_calls[0]
        structured_data = tool_call.function.arguments

        return ChatResponse(
            role="bot",
            content_type="json",
            content=structured_data
        )
