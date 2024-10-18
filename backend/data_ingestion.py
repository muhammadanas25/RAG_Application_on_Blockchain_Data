# backend/data_ingestion.py

import os
from moralis import evm_api
from backend.models.transaction import Transaction
from backend.models.block import Block
from backend.models.log import Log
from backend.services.database import SessionLocal, engine, Base
from backend.core.config import settings

def create_tables():
    Base.metadata.create_all(bind=engine)

def ingest_block_data(block_numbers):
    api_key = settings.MORALIS_API_KEY
    session = SessionLocal()

    for block_number in block_numbers:
        try:
            params = {
                "block_number_or_hash": str(block_number),
                "chain": "eth"
            }

            block_data = evm_api.block.get_block(
                api_key=api_key,
                params=params,
            )

            # Create Block object
            block = Block(
                number=int(block_data.get('number')),
                hash=block_data.get('hash'),
                parent_hash=block_data.get('parent_hash'),
                timestamp=block_data.get('timestamp'),
                miner=block_data.get('miner'),
                difficulty=int(block_data.get('difficulty', '0')),
                total_difficulty=int(block_data.get('total_difficulty', '0')),
                size=int(block_data.get('size', '0')),
                gas_limit=int(block_data.get('gas_limit', '0')),
                gas_used=int(block_data.get('gas_used', '0')),
                # Include additional fields as needed
            )

            session.merge(block)

            transactions = block_data.get('transactions', [])
            for tx_data in transactions:
                transaction = Transaction(
                    tx_hash=tx_data.get('hash'),
                    nonce=int(tx_data.get('nonce', '0')),
                    transaction_index=int(tx_data.get('transaction_index', '0')),
                    from_address=tx_data.get('from_address'),
                    to_address=tx_data.get('to_address'),
                    value=int(tx_data.get('value', '0')),
                    gas=int(tx_data.get('gas', '0')),
                    gas_price=int(tx_data.get('gas_price', '0')),
                    input=tx_data.get('input'),
                    receipt_cumulative_gas_used=int(tx_data.get('receipt_cumulative_gas_used', '0')),
                    receipt_gas_used=int(tx_data.get('receipt_gas_used', '0')),
                    receipt_contract_address=tx_data.get('receipt_contract_address'),
                    receipt_status=int(tx_data.get('receipt_status', '0')),
                    block_timestamp=tx_data.get('block_timestamp'),
                    block_number=int(tx_data.get('block_number', '0')),
                    block_hash=tx_data.get('block_hash'),
                    # Include additional fields as needed
                )

                session.merge(transaction)

                logs = tx_data.get('logs', [])
                for log_data in logs:
                    log = Log(
                        log_index=int(log_data.get('log_index', '0')),
                        transaction_hash=log_data.get('transaction_hash'),
                        transaction_index=int(log_data.get('transaction_index', '0')),
                        address=log_data.get('address'),
                        data=log_data.get('data'),
                        topic0=log_data.get('topic0'),
                        topic1=log_data.get('topic1'),
                        topic2=log_data.get('topic2'),
                        topic3=log_data.get('topic3'),
                        block_timestamp=log_data.get('block_timestamp'),
                        block_number=int(log_data.get('block_number', '0')),
                        block_hash=log_data.get('block_hash'),
                        # Include additional fields as needed
                    )

                    session.merge(log)

            session.commit()
            print(f"Successfully ingested block {block_number}")

        except Exception as e:
            session.rollback()
            print(f"Error ingesting block {block_number}: {str(e)}")

    session.close()

if __name__ == "__main__":
    # Create tables if they do not exist
    create_tables()

    # Specify the block numbers you want to ingest
    block_numbers = [20950668,20979704,20979703,20979702,20979701,20979700]  # Add more block numbers as needed

    # Ingest block data
    ingest_block_data(block_numbers)
