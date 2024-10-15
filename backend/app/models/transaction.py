# app/models/transaction.py
from sqlalchemy import create_engine, Column, Integer, String, Float,Numeric
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


Base = declarative_base()

class Transaction(Base):
    __tablename__ = 'transactions'

    tx_hash = Column(String, primary_key=True, index=True)
    method = Column(String, nullable=True)
    from_address = Column(String, index=True)
    to_address = Column(String, index=True)
    amount = Column(Numeric, nullable=False)
    tx_fee = Column(Numeric, nullable=False)
    block_number = Column(Integer, index=True)

engine = create_engine('postgresql://anas:anas123@localhost:5432/blockchain_db')

# Create all tables in the engine. This is equivalent to "Create Table"
# statements in raw SQL.
Base.metadata.create_all(engine)

# Create a session
Session = sessionmaker(bind=engine)
session = Session()