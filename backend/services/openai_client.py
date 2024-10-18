# backend/services/openai_client.py

import openai
from backend.core.config import settings
from openai import OpenAI
class OpenAIClient:
    def __init__(self):
       # openai.api_key = settings.OPENAI_API_KEY
        self.client = OpenAI(api_key=settings.OPENAI_API_KEY)

    def generate(self, messages: list, functions: list = None) -> dict:
        response = self.client.chat.completions.create(model="gpt-4",
            messages=messages,
            functions=functions,
            temperature=0.2
        )

    
        return response
