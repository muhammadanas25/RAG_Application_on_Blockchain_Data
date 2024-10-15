# app/services/openai_client.py

from openai import OpenAI

from app.core.config import settings

class OpenAIClient:
    def __init__(self):
        self.client = OpenAI(api_key=settings.OPENAI_API_KEY)

    def generate_sql_query(self, natural_language_query: str, schema_description: str):
        prompt = f"""
You are an expert SQL assistant.

Given the following database schema:
{schema_description}

Translate the user's natural language query into a syntactically correct SQL query that can be executed on a PostgreSQL database.

Make sure to:
- Use appropriate SQL syntax for PostgreSQL.
- Sanitize any user inputs to prevent SQL injection.
- Return only the SQL query without any explanation.

User Query: "{natural_language_query}"
SQL Query:
"""
        response = self.client.completions.create(
            model="gpt-3.5-turbo-instruct",
            prompt=prompt,
            max_tokens=200,
            temperature=0.5,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0,
            stop=["#", ";"]  # Stops the output after the SQL query
        )
        sql_query = response.choices[0].text.strip()
        return sql_query
