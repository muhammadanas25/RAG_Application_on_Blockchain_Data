# backend/functions/data_retrieval.py

from backend.services.database import SessionLocal
from backend.models.transaction import Transaction
from backend.models.block import Block

def check_transaction_exists(tx_hash: str) -> bool:
    session = SessionLocal()
    exists = session.query(Transaction).filter_by(tx_hash=tx_hash).first() is not None
    session.close()
    return exists

def get_transaction_details(tx_hash: str) -> dict:
    session = SessionLocal()
    transaction = session.query(Transaction).filter_by(tx_hash=tx_hash).first()
    session.close()
    if transaction:
        return {
            "tx_hash": transaction.tx_hash,
            "from_address": transaction.from_address,
            "to_address": transaction.to_address,
            "value": float(transaction.value),
            "block_number": transaction.block_number,
            "gas": float(transaction.gas),
            "gas_price": float(transaction.gas_price),
            # Include additional fields as needed
        }
    else:
        return {}

def get_transactions_by_sender_in_block(from_address: str, block_number: int) -> list:
    session = SessionLocal()
    transactions = session.query(Transaction).filter_by(
        from_address=from_address,
        block_number=block_number
    ).all()
    session.close()
    return [
        {
            "tx_hash": tx.tx_hash,
            "to_address": tx.to_address,
            "value": float(tx.value),

            # Include additional fields as needed
        }
        for tx in transactions
    ]

def get_block_transactions(block_number: int) -> list:
    session = SessionLocal()
    transactions = session.query(Transaction).filter_by(block_number=block_number).all()
    session.close()
    return [
        {
            "tx_hash": tx.tx_hash,
            "from_address": tx.from_address,
            "to_address": tx.to_address,
            "value": float(tx.value),
            "gas": float(tx.gas),
            "gas_price": float(tx.gas_price),
            # Include additional fields as needed
        }
        for tx in transactions
    ]

def get_blocks_in_range(start_block: int, end_block: int) -> list:
    session = SessionLocal()
    blocks = session.query(Block).filter(
        Block.number >= start_block,
        Block.number <= end_block
    ).all()
    session.close()
    return [
        {
            "number": block.number,
            "hash": block.hash,
            "timestamp": block.timestamp,
            # Include additional fields as needed
        }
        for block in blocks
    ]
