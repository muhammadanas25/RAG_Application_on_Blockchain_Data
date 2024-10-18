# backend/models/block.py

from sqlalchemy import Column, String, Integer, Numeric, DateTime, BigInteger
from backend.services.database import Base

class Block(Base):
    __tablename__ = 'blocks'

    number = Column(Integer, primary_key=True)
    hash = Column(String, unique=True)
    parent_hash = Column(String)
    nonce = Column(String)
    sha3_uncles = Column(String)
    logs_bloom = Column(String)
    transactions_root = Column(String)
    state_root = Column(String)
    receipts_root = Column(String)
    miner = Column(String)
    difficulty = Column(BigInteger)
    total_difficulty = Column(BigInteger)
    size = Column(BigInteger)
    extra_data = Column(String)
    gas_limit = Column(BigInteger)
    gas_used = Column(BigInteger)
    timestamp = Column(DateTime)
    transaction_count = Column(Integer)
    base_fee_per_gas = Column(BigInteger)
    # Additional fields can be added as needed
