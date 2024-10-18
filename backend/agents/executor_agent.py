# backend/agents/executor_agent.py

from backend.functions import data_retrieval, computations
from backend.utils import mapping_utils
import time

class ExecutorAgent:
    def execute(self, steps: list) -> dict:
        results = {}
        for step in steps:
            function_name, args = mapping_utils.map_step_to_function(step)
            function = getattr(data_retrieval, function_name, None) or getattr(computations, function_name, None)
            if function:
                attempt = 0
                while attempt < 3:
                    try:
                        result = function(**args)
                        results[step] = result
                        break
                    except Exception as e:
                        attempt += 1
                        time.sleep(2 ** attempt)  # Exponential backoff
                else:
                    results[step] = {'error': f"Failed after 3 attempts: {str(e)}"}
            else:
                results[step] = {'error': f"Function {function_name} not found."}
        return results
