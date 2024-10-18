# app/services/vector_db.py
import uuid
from qdrant_client import QdrantClient
from qdrant_client.http import models
from app.core.config import settings
from openai import OpenAI

class VectorDBClient:
    def __init__(self):
        # Initialize Qdrant client
        self.client = QdrantClient(host='localhost', port=6333)
        self.collection_name = 'transactions'

        # Initialize OpenAI client
        self.openai_client = OpenAI(api_key=settings.OPENAI_API_KEY)

        # Define the collection if it doesn't exist
        if self.collection_name not in [col.name for col in self.client.get_collections().collections]:
            self.client.recreate_collection(
                collection_name=self.collection_name,
                vectors_config=models.VectorParams(size=1536, distance=models.Distance.COSINE)
            )

    def upsert_transaction(self, tx_hash: str, text: str):
        # Generate embedding using OpenAI
        embedding = self.get_embedding(text)

        # Convert tx_hash to UUID
        tx_hash_uuid = str(uuid.uuid5(uuid.NAMESPACE_OID, tx_hash))

        # Prepare the point to insert
        point = models.PointStruct(
            id=tx_hash_uuid,
            vector=embedding,
            payload={'tx_hash': tx_hash}
        )

        # Upsert the point into the collection
        self.client.upsert(
            collection_name=self.collection_name,
            points=[point]
        )

    def query_similar_transactions(self, query_text: str, top_k: int = 5):
        # Generate embedding for the query
        query_embedding = self.get_embedding(query_text)

        # Perform search in Qdrant
        search_result = self.client.search(
            collection_name=self.collection_name,
            query_vector=query_embedding,
            limit=top_k
        )

        return search_result

    def get_embedding(self, text: str):
        # Generate embedding using OpenAI's API
        response = self.openai_client.embeddings.create(
            input=text,
            model='text-embedding-ada-002'
        )
        embedding = response.data[0].embedding
        return embedding

    
    def search_embeddings(self, query_embedding, top_k=5):
        # Perform search in Qdrant
        search_result = self.client.search(
            collection_name=self.collection_name,
            query_vector=query_embedding,
            limit=top_k,
            with_payload=True  # Include payload in results
        )
        return search_result