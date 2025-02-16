from fastapi import FastAPI
from fastapi import FastAPI, HTTPException, Body

from llm_app import llm_agent

app = FastAPI()

@app.post("/chat")
async def chat(params: dict = Body()):
    question = params.get("question")
    if question is None:
        raise HTTPException(422, "No question provided")

    inputs = {
        "input": question + "",
        "feedbacks": []
    }

    events = []

    for event in llm_agent.stream(inputs):
        print(event)
        events.append(event)

    if len(events) == 0:
        return {"response": "I only answer nmap and subdomain related questions."}

    response = events[-1]["wrapper"]["response"]

    return {"response": response}
