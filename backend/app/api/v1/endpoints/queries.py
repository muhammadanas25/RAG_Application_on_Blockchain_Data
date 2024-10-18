# app/api/v1/endpoints/queries.py

from fastapi import APIRouter, HTTPException, Request
from app.services.query_processor import QueryProcessor
from pydantic import BaseModel
import logging

logger = logging.getLogger(__name__)
router = APIRouter()
query_processor = QueryProcessor()

class QueryRequest(BaseModel):
    query: str

@router.post("/query")
def process_query(request: QueryRequest):
    logger.info(f"Processing query: {request.query}")
    print(f"Processing query: {request.query}")
    result = query_processor.process_query(request.query)
    logger.info(f"Query result: {result}")
    print(f"Query result: {result}")
    if "error" in result:
        raise HTTPException(status_code=400, detail="error in query processing")
    return result