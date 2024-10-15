# data_ingestion.py

import csv
import glob
import os
from app.services.moralis_service import MoralisClient
from app.db.session import SessionLocal
from app.models.transaction import Transaction
from app.services.vector_db import VectorDBClient

def ingest_blocks_from_csvs(csv_folder_path):
    # Initialize services
    moralis_client = MoralisClient()
    vector_db_client = VectorDBClient()
    db_session = SessionLocal()

    # Get all CSV files in the specified folder
    csv_files = glob.glob(os.path.join(csv_folder_path, "*.csv"))
    print("--------",csv_files)
    block_numbers = set()

    # Read block numbers from all CSV files
    for csv_file in csv_files:
        print("--------",csv_file)
        with open(csv_file, mode='r') as file:
            reader = csv.reader(file)
            header = next(reader)  # Skip header if present
            for row in reader:
                # Assuming block number is in the first column; adjust index as needed
                block_number = row[3].strip()
                if block_number.isdigit():
                    block_numbers.add(int(block_number))

    print(f"Found {len(block_numbers)} unique block numbers.")

    # Fetch and store transactions for each block number
    for block_number in block_numbers:
        print(f"Processing block number: {block_number}")
        try:
            block_data = moralis_client.get_block_transactions(block_number_or_hash=str(block_number))

            transactions = block_data.get('transactions', [])
            print(f"Found {len(transactions)} transactions in block {block_number}.")

            for tx in transactions:
                # Create Transaction object
                transaction = Transaction(
                    tx_hash=tx.get('hash'),
                    method=tx.get('input'),  # Adjust if you have method parsing
                    from_address=tx.get('from_address'),
                    to_address=tx.get('to_address'),
                    amount=int(tx.get('value', '0')) / 1e18,  # Convert wei to ETH
                    tx_fee=(int(tx.get('gas', '0')) * int(tx.get('gas_price', '0'))) / 1e18,
                    block_number=int(tx.get('block_number'))
                )

                # Add to database session
                db_session.merge(transaction)

                # Prepare text for embedding (customize as needed)
                tx_text = f"Transaction {transaction.tx_hash} from {transaction.from_address} to {transaction.to_address} of {transaction.amount} ETH"

                # Upsert into vector database
                vector_db_client.upsert_transaction(tx_hash=transaction.tx_hash, text=tx_text)

            # Commit the session after processing each block
            db_session.commit()

        except Exception as e:
            print(f"Error processing block {block_number}: {e}")
            continue

    # Close the database session
    db_session.close()

if __name__ == "__main__":
    # Specify the folder path containing CSV files
    csv_folder = "/home/anassiddiqui/AI-blockchain/backend/app/data/csv_blocks"

    ingest_blocks_from_csvs(csv_folder)
