from typing import Literal
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from pydantic import BaseModel, Field


# Data model for user feedback validation
class UserFeedbackQuery(BaseModel):
    """Determines if a user is satisfied with a generated Linux command."""

    satisfied: Literal["yes", "no"] = Field(
        ...,
        description="If the user provides feedback, answer 'no'. Otherwise, answer 'yes'.",
    )

    feedback: str = Field(
        description="Reword user feedback into a precise, actionable suggestion.",
    )


# Define correct command syntax references
COMMAND_SYNTAX = """
- **Sublist3r**: `sublist3r -d <domain> [-o <output_file>]`
- **Nmap**: `nmap [-options] <target>`
"""

# System prompt with refined structure
system_prompt = f"""You are an expert at verifying Linux commands for security tools.
Your task is to determine whether the generated command correctly satisfies the user's intent.

### Steps:
 1. **Analyze the user's question** to determine the expected command structure.
 2. If there are no feedbacks, or the feedback is 'continue', 'next', then user is satisfied.
"""

# LangChain prompt template
matcher_prompt = ChatPromptTemplate.from_messages(
    [
        ("system", system_prompt),
        ("human", "Feedback: {feedback}\nGenerated command:\n{generated_command}"),
    ]
)


# Chain function to check syntax using LangChain
def get_user_checker(llm: ChatOpenAI) -> ChatPromptTemplate:
    """Returns a structured syntax checker using LangChain."""
    return matcher_prompt | llm.with_structured_output(UserFeedbackQuery)
