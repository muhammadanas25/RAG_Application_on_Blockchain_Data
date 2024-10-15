# app/services/query_processor.py

from app.services.openai_client import OpenAIClient
from app.services.vector_db import VectorDBClient
from app.db.session import SessionLocal
from sqlalchemy.exc import SQLAlchemyError
from app.core.config import settings
from app.models.transaction import Transaction
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class QueryProcessor:
    def __init__(self):
        self.openai_client = OpenAIClient()
        self.vector_db_client = VectorDBClient()
        self.db_session = SessionLocal()

    def process_query(self, natural_language_query: str):
        schema_description = """
        Table transactions:
        - tx_hash (String, Primary Key)
        - method (String)
        - from_address (String)
        - to_address (String)
        - amount (Numeric)
        - tx_fee (Numeric)
        - block_number (Integer)
        """

        max_retries = 3
        for attempt in range(max_retries):
            try:
                logger.info(f"Attempt {attempt + 1} to generate SQL query.")
                sql_query = self.openai_client.generate_sql_query(natural_language_query, schema_description)
                logger.info(f"Generated SQL query: {sql_query}")

                # Validate and sanitize the SQL query here if necessary

                # Execute the SQL query
                result = self.db_session.execute(sql_query).fetchall()
                logger.info("SQL query executed successfully.")
                return {"method": "sql", "result": result}
            except (SQLAlchemyError, Exception) as e:
                logger.warning(f"SQL query failed on attempt {attempt + 1}: {e}")
                # Optionally, modify the prompt or the query before retrying
                continue  # Try again

        # Fallback to vector database
        logger.info("Falling back to vector database search.")
        try:
            search_results = self.vector_db_client.query_similar_transactions(natural_language_query, top_k=5)
            # Extract transaction IDs from search results
            tx_hashes = [str(hit.id) for hit in search_results]

            # Fetch transactions from the database
            transactions = self.db_session.query(Transaction).filter(Transaction.tx_hash.in_(tx_hashes)).all()
            logger.info("Retrieved transactions from vector database search.")
            return {"method": "vector_db", "result": transactions}
        except Exception as e:
            logger.error(f"Failed to retrieve results from vector database: {e}")
            return {"error": "Unable to process the query at this time."}
        finally:
            self.db_session.close()
