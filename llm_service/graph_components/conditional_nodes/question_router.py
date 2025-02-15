from typing import Literal

from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI

from pydantic import BaseModel, Field


# Data model
class RouteQuery(BaseModel):
    """Route a user query to the most relevant datasource."""

    datasource: Literal["command_generator", "not_relevant"] = Field(
        ...,
        description="Given a user question choose to route it to command_generator or not_relevant.",
    )


# Prompt
system = """You are an expert at routing a user question to a linux command generator or a default (not_relevant) node in langgraph.
The command generator can only work with the following commands (Nmap, Sublist3r), no other command would work. 
If the question doesn't mention any of the listed linux libraries then the question isn't relevant."""

route_prompt = ChatPromptTemplate.from_messages(
    [
        ("system", system),
        ("human", "{question}"),
    ]
)

def get_question_router(llm: ChatOpenAI):
    return route_prompt | llm.with_structured_output(RouteQuery)
