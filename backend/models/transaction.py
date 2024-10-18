# backend/models/transaction.py

from sqlalchemy import Column, String, Numeric, Integer, DateTime, BigInteger
from backend.services.database import Base

class Transaction(Base):
    __tablename__ = 'transactions'

    tx_hash = Column(String, primary_key=True, index=True)
    nonce = Column(BigInteger)
    transaction_index = Column(Integer)
    from_address = Column(String, index=True)
    to_address = Column(String, index=True)
    value = Column(Numeric)
    gas = Column(BigInteger)
    gas_price = Column(BigInteger)
    input = Column(String)
    receipt_cumulative_gas_used = Column(BigInteger)
    receipt_gas_used = Column(BigInteger)
    receipt_contract_address = Column(String)
    receipt_root = Column(String)
    receipt_status = Column(Integer)
    block_timestamp = Column(DateTime)
    block_number = Column(Integer, index=True)
    block_hash = Column(String)
    # Additional fields can be added as needed
