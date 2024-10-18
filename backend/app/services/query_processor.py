# app/services/query_processor.py
from app.services.vector_db import VectorDBClient
from app.db.session import SessionLocal
from app.core.config import settings
from app.models.transaction import Transaction
from openai import OpenAIError
from openai import OpenAI
import openai

class QueryProcessor:
    def __init__(self):
        self.vector_db_client = VectorDBClient()
        self.db_session = SessionLocal()
        openai.api_key = settings.OPENAI_API_KEY
        self.client = OpenAI(api_key=settings.OPENAI_API_KEY)

    def process_query(self, user_query: str):
        # Step 1: Generate embedding for the user query
        query_embedding = self.vector_db_client.get_embedding(user_query)

        # Step 2: Perform semantic search in Qdrant
        search_results = self.vector_db_client.search_embeddings(query_embedding)

        if not search_results:
            return "No relevant data found for your query."

        # Step 3: Retrieve detailed data from PostgreSQL
        transaction_ids = [result.payload['tx_hash'] for result in search_results]
        transactions = self.get_transactions_by_ids(transaction_ids)
        print("transactions",transactions)
        # Step 4: Construct context for OpenAI API
        context = self.construct_context(transactions)
        print("context",context)
        # Step 5: Generate response using OpenAI Chat Completion API
        response = self.generate_response(user_query, context)

        return response

    def get_transactions_by_ids(self, tx_ids):
        return self.db_session.query(Transaction).filter(Transaction.tx_hash.in_(tx_ids)).all()

    def construct_context(self, transactions):
        # Format transactions into a readable context
        context = "\n".join([
            f"Transaction {tx.tx_hash}:\n"
            f"  From: {tx.from_address}\n"
            f"  To: {tx.to_address}\n"
            f"  Amount: {tx.amount} ETH\n"
            f"  Block Number: {tx.block_number}\n"
            f"  Transaction Fee: {tx.tx_fee} ETH\n"
            for tx in transactions
        ])
        return context

    def generate_response(self, user_query, context):
        messages = [
            {"role": "system", "content": "You are a blockchain expert assistant."},
            {"role": "user", "content": user_query},
            {"role": "assistant", "content": f"Here is some relevant data:\n{context}"},
            {"role": "assistant", "content": "Based on the data above, here's the answer to your query:"}
        ]
        try:
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=messages,
                max_tokens=500,
                temperature=0.7
            )
            print(response)
            return response.choices[0].message
        except OpenAIError as e:
            return f"An error occurred while generating the response: {e}"
