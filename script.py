import requests
import pandas as pd
from moralis import evm_api

# Load the CSV file containing transaction data
file_path = 'export-transaction-list-1728752846969.csv'
df = pd.read_csv(file_path)
print(df.head())
# Your Moralis API key
api_key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJub25jZSI6IjRkYzlmODQ0LTE0N2UtNDMxOS1hNTY0LTUzMjJlY2UyMjQ4MSIsIm9yZ0lkIjoiNDExNzk1IiwidXNlcklkIjoiNDIzMTgxIiwidHlwZUlkIjoiNGQyMzVjNTAtYjcyNS00ZDliLWE1NWYtNjg3NDkyN2JkMTRjIiwidHlwZSI6IlBST0pFQ1QiLCJpYXQiOjE3Mjg5NDA5MjcsImV4cCI6NDg4NDcwMDkyN30.6TqAtbsxvMN89CLxnjYZrzh727hpxLhLRtUtMahsZzc"

# Function to fetch block data using Moralis API
def fetch_block_data(block_number):
    params = {
        "block_number_or_hash": block_number,
        "chain": "eth"
    }
    try:
        result = evm_api.block.get_block(api_key=api_key, params=params)
        return result
    except Exception as e:
        print(f"Error fetching block {block_number}: {e}")
        return None

# Example: Fetching block data for all block numbers in the CSV
for block_number in df['Blockno'].unique():
    print(block_number)
    block_data = fetch_block_data(str(block_number))
    if block_data:
        print(f"Block {block_number} data: {block_data}")
input("Press Enter to continue...")
# Function to find similar transactions based on block data
def find_similar_transactions(df, block_number, similarity_criteria):
    # Get all transactions from the specified block number
    target_block_data = df[df['Blockno'] == block_number]
    if target_block_data.empty:
        print(f"No transactions found for block {block_number}")
        return
    
    # Example: Similarity based on method and amount
    similar_transactions = df[
        (df['Method'] == similarity_criteria['method']) &
        (df['Amount'] == similarity_criteria['amount'])
    ]
    return similar_transactions

# Example usage
block_number = 20950668
similarity_criteria = {
    'method': 'Transfer',
    'amount': '0.01907202 ETH'
}

similar_txns = find_similar_transactions(df, block_number, similarity_criteria)
print(similar_txns)

# Function to filter transactions with high gas usage
def filter_high_gas_usage(df, gas_threshold):
    high_gas_txns = df[df['Txn Fee'] > gas_threshold]
    return high_gas_txns

# Example usage
gas_threshold = 0.0015  # Adjust threshold as per your requirement
high_gas_transactions = filter_high_gas_usage(df, gas_threshold)
print(high_gas_transactions)

# Function to calculate average transaction fee in a block range
def calculate_average_fee(df, start_block, end_block):
    block_range_data = df[(df['Blockno'] >= start_block) & (df['Blockno'] <= end_block)]
    avg_fee = block_range_data['Txn Fee'].mean()
    return avg_fee

# Example usage
start_block = 20950000
end_block = 20950668
avg_fee = calculate_average_fee(df, start_block, end_block)
print(f"Average transaction fee from block {start_block} to {end_block}: {avg_fee}")
