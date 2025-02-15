from typing import Literal
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from pydantic import BaseModel, Field


# Data model
class CommandQuery(BaseModel):
    """Route a user query to the most relevant datasource."""

    matches_user_input: Literal["yes", "no"] = Field(
        ...,
        description="Given a user question, a generated linux command, list of feedbacks, and command execution output, determine if the command correctly matches the user's intent and adheres to the provided feedback.",
    )

    feedback: str = Field(
        description="""
        Given a user question, a generated linux command, a list of feedback messages, and the command execution output, provide specific feedback on necessary improvements.

        - If a flag or argument is incorrect or missing, suggest the exact correction.
        - If the command structure is wrong, provide the corrected syntax.
        - If additional context is needed, explain briefly.
        - If the command is correct, return an empty string.
        """,
    )


# Correct Command Syntax Reference (escaped as a string)
COMMAND_SYNTAX = """
- **Sublist3r**: `sublist3r -d <domain> [-o <output_file>]`
- **Nmap**: `nmap [-options] <target>`
"""

# System Prompt (Fixed)
system = f"""You are an expert at verifying Linux commands for security tools.
You will determine whether the command correctly matches the user's intent and adheres to the provided feedback messages.

### Steps:
1. **Compare the command** to the correct syntax for the relevant tool:
{COMMAND_SYNTAX}
2. **If the command is incorrect**, specify exactly what is wrong:
   - Suggest the correct flag(s) or arguments.
   - Provide an example correction.
3. **If the command is correct**, return an empty feedback string.

### Response Format:
- If incorrect: Explain the issue and provide the corrected command.
- If correct: Return an empty string.
"""

# LangChain prompt template
matcher_prompt = ChatPromptTemplate.from_messages(
    [
        ("system", system),
        ("human",
         "User question: {question}\nFeedback:\n{feedback_list}\nGenerated command:\n{generated_command}\nCommand output:\n{command_output}"),
    ]
)


# Chain
def get_matcher(llm: ChatOpenAI):
    return matcher_prompt | llm.with_structured_output(CommandQuery)
