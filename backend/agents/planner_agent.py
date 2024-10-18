# backend/agents/planner_agent.py

from backend.services.openai_client import OpenAIClient

class PlannerAgent:
    def __init__(self):
        self.llm = OpenAIClient()

    def plan(self, user_query: str) -> list:
        messages = [
            {"role": "system", "content": "You are a planning assistant that creates a step-by-step plan to fulfill the user's request."},
            {"role": "user", "content": user_query}
        ]

        response = self.llm.generate(messages)
        plan_text = response['choices'][0]['message']['content'].strip()
        steps = parse_plan_text(plan_text)
        return steps
