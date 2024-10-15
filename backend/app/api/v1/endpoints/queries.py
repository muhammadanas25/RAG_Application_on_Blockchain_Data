# app/api/v1/endpoints/queries.py

from fastapi import APIRouter, HTTPException, Request
from app.services.query_processor import QueryProcessor
from pydantic import BaseModel

router = APIRouter()
query_processor = QueryProcessor()

class QueryRequest(BaseModel):
    query: str

@router.post("/query")
def process_query(request: QueryRequest):
    result = query_processor.process_query(request.query)
    if "error" in result:
        raise HTTPException(status_code=400, detail=result["error"])
    return result