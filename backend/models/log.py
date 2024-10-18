# backend/models/log.py

from sqlalchemy import Column, String, Integer, DateTime, BigInteger
from backend.services.database import Base

class Log(Base):
    __tablename__ = 'logs'

    id = Column(Integer, primary_key=True, autoincrement=True)
    log_index = Column(Integer)
    transaction_hash = Column(String, index=True)
    transaction_index = Column(Integer)
    address = Column(String)
    data = Column(String)
    topic0 = Column(String)
    topic1 = Column(String)
    topic2 = Column(String)
    topic3 = Column(String)
    block_timestamp = Column(DateTime)
    block_number = Column(Integer)
    block_hash = Column(String)
    # Additional fields can be added as needed
