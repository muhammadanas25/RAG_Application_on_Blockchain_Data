# app/main.py
from fastapi import FastAPI
from app.api.v1.endpoints import transactions, queries

app = FastAPI(
    title="Blockchain Query API",
    version="1.0.0"
)

app.include_router(transactions.router, prefix="/api/v1", tags=["transactions"])
app.include_router(queries.router, prefix="/api/v1", tags=["queries"])
