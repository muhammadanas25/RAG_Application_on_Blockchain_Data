# app/api/v1/endpoints/transactions.py
from fastapi import APIRouter, HTTPException
from app.models.transaction import Transaction
from app.db.session import SessionLocal

router = APIRouter()

@router.get("/transaction/{tx_hash}")
def get_transaction(tx_hash: str):
    db = SessionLocal()
    transaction = db.query(Transaction).filter(Transaction.tx_hash == tx_hash).first()
    if not transaction:
        raise HTTPException(status_code=404, detail="Transaction not found")
    return transaction
