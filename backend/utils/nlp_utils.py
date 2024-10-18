# backend/utils/nlp_utils.py

import re

def extract_entities(user_query: str) -> dict:
    entities = {}
    # Regex to extract transaction hash
    tx_hash_match = re.search(r'(0x[a-fA-F0-9]{64})', user_query)
    if tx_hash_match:
        entities['tx_hash'] = tx_hash_match.group(1)
    # Add more extraction logic as needed
    return entities

def parse_plan_text(plan_text: str) -> list:
    steps = plan_text.strip().split('\n')
    steps = [step.strip('- ').strip() for step in steps if step.strip()]
    return steps
