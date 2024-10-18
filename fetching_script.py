import requests
import pandas as pd
from moralis import evm_api
import json
# ... existing code ...

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

# List of specific block numbers to fetch
block_numbers = [20979704, 20979703, 20979702, 20979701, 20979700]

# Fetch and print block data for specified block numbers
for block_number in block_numbers:
    print(f"\nFetching data for block {block_number}")
    block_data = fetch_block_data(str(block_number))
    if block_data:
        print(f"Block {block_number} data:")
        print(json.dumps(block_data, indent=2))
        
        # List all keys in the JSON structure
        print(f"\nKeys in the JSON structure for block {block_number}:")
        for key in block_data.keys():
            print(f"- {key}")
        
        # If there are nested dictionaries, you might want to explore them as well
        if 'transactions' in block_data and block_data['transactions']:
            print("\nKeys in the first transaction:")
            for key in block_data['transactions'][0].keys():
                print(f"- {key}")

    input("Press Enter to continue...")
# ... rest of the existing code ...