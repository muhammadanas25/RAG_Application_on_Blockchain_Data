# backend/functions/computations.py

from backend.functions.data_retrieval import get_block_transactions

def calculate_total_transaction_value(transactions: list) -> float:
    total_value = sum(tx['value'] for tx in transactions)
    return total_value

def find_block_with_highest_total_value(block_numbers: list) -> dict:
    highest_value = 0
    highest_block_number = None
    for block_number in block_numbers:
        transactions = get_block_transactions(block_number)
        total_value = calculate_total_transaction_value(transactions)
        if total_value > highest_value:
            highest_value = total_value
            highest_block_number = block_number
    if highest_block_number is not None:
        return {
            'block_number': highest_block_number,
            'total_value': highest_value
        }
    else:
        return {}
