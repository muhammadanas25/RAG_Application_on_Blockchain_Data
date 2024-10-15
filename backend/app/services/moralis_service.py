# app/services/moralis.py
import requests
from moralis import evm_api
#from app.core.config import settings

class MoralisClient:

    def __init__(self):
        # self.api_key = settings.MORALIS_API_KEY
         self.api_key = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJub25jZSI6IjRkYzlmODQ0LTE0N2UtNDMxOS1hNTY0LTUzMjJlY2UyMjQ4MSIsIm9yZ0lkIjoiNDExNzk1IiwidXNlcklkIjoiNDIzMTgxIiwidHlwZUlkIjoiNGQyMzVjNTAtYjcyNS00ZDliLWE1NWYtNjg3NDkyN2JkMTRjIiwidHlwZSI6IlBST0pFQ1QiLCJpYXQiOjE3Mjg5NDA5MjcsImV4cCI6NDg4NDcwMDkyN30.6TqAtbsxvMN89CLxnjYZrzh727hpxLhLRtUtMahsZzc'
    def get_block_transactions(self, block_number_or_hash: str):
        params = {
            "block_number_or_hash": str(block_number_or_hash),
            "chain": "eth"
        }
        result = evm_api.block.get_block(
            api_key=self.api_key,
            params=params,
        )
        return result

# Example usage
if __name__ == "__main__":
    moralis_client = MoralisClient()
    block_transactions = moralis_client.get_block_transactions(123456)
    print(block_transactions)
