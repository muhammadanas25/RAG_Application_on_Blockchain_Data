# backend/agents/responder_agent.py

from backend.services.openai_client import OpenAIClient
import json
class ResponderAgent:
    def respond(self, user_query: str, execution_results: dict) -> str:
        context = f"Execution Results:\n{execution_results}"
        prompt = f"""
{context}

Based on the above execution results, provide a detailed and accurate response to the user's query: "{user_query}"

Ensure that the response is clear, concise, and based solely on the execution results. Do not include any information not present in the execution results.
"""
        response = OpenAIClient().generate(prompt)
        return response
def respond(self, user_query: str, execution_results: dict) -> str:
    messages = [
        {"role": "system", "content": "You are an AI assistant that provides detailed and accurate responses based on execution results."},
        {"role": "user", "content": user_query}
    ]

    functions = [
        {
            "name": "get_transaction_details",
            "description": "Retrieves details of a transaction by its hash.",
            "parameters": {
                "type": "object",
                "properties": {
                    "tx_hash": {"type": "string", "description": "The transaction hash."}
                },
                "required": ["tx_hash"]
            }
        },
        # Add more functions as needed
    ]

    response = OpenAIClient().generate(messages, functions)
    message = response['choices'][0]['message']

    # Check if the assistant wants to call a function
    if message.get("function_call"):
        function_name = message["function_call"]["name"]
        function_args = json.loads(message["function_call"]["arguments"])

        # Call the function
        if function_name == "get_transaction_details":
            function_response = get_transaction_details(**function_args)
            # Append the function response to messages
            messages.append({
                "role": "function",
                "name": function_name,
                "content": json.dumps(function_response)
            })
            # Generate the final response
            final_response = OpenAIClient().generate(messages)
            return final_response['choices'][0]['message']['content'].strip()
    else:
        # No function call needed
        return message['content'].strip()
