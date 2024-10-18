# backend/main.py

from fastapi import FastAPI, Request
from pydantic import BaseModel
from backend.agents.prompt_verification_agent import PromptVerificationAgent
from backend.agents.planner_agent import PlannerAgent
from backend.agents.executor_agent import ExecutorAgent
from backend.agents.responder_agent import ResponderAgent

app = FastAPI()

class QueryRequest(BaseModel):
    query: str

@app.post("/query")
async def process_query(request: QueryRequest):
    user_query = request.query

    # Step 1: Prompt Verification
    verification_agent = PromptVerificationAgent()
    verification_results = verification_agent.verify_query(user_query)

    if not all(verification_results.values()):
        missing_entities = [k for k, v in verification_results.items() if not v]
        return {"message": f"Data not found for entities: {', '.join(missing_entities)}"}

    # Step 2: Planning
    planner_agent = PlannerAgent()
    plan_steps = planner_agent.plan(user_query)

    # Step 3: Execution
    executor_agent = ExecutorAgent()
    execution_results = executor_agent.execute(plan_steps)

    # Step 4: Response Generation
    responder_agent = ResponderAgent()
    response = responder_agent.respond(user_query, execution_results)

    return {"response": response}
