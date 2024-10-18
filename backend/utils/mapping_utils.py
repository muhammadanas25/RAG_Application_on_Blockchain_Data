# backend/utils/mapping_utils.py

def map_step_to_function(step: str):
    # Simplistic mapping based on keywords
    if "check if transaction exists" in step:
        return "check_transaction_exists", {}
    elif "get transaction details" in step:
        return "get_transaction_details", {}
    elif "find block with highest total value" in step:
        return "find_block_with_highest_total_value", {}
    # Add more mappings as needed
    else:
        return None, {}
