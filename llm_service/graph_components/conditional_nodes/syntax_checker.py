from typing import Literal
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from pydantic import BaseModel, Field


# Data model
class SyntaxQuery(BaseModel):
    """Route a user query to the most relevant datasource."""

    matches_user_input: Literal["yes", "no"] = Field(
        ...,
        description="""
        Given a user question, a generated Linux command, and a list of feedback messages, 
        determine if the command correctly matches the user's intent and adheres to the provided feedback.
        """,
    )

    feedback: str = Field(
        description="""
        Given a user question, a generated Linux command, and a list of feedback messages, 
        provide specific feedback on necessary improvements.

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

system = f"""You are an expert at verifying Linux commands for security tools.
Your task is to determine whether the generated command:
- **Correctly matches the user's intent** based on their question.
- **Includes all necessary tools and flags** to fulfill the request.
- **Adheres to feedback messages** if any are provided.

### Steps:
1. **Analyze the user's question** to determine what actions are required.
2. **Compare the command** to the correct syntax for the relevant tools:
{COMMAND_SYNTAX}
3. **Ensure all parts of the user's intent are fulfilled**:
   - If the user asks for multiple tasks (e.g., scanning ports and finding subdomains), check that the command includes the necessary tools (`nmap`, `sublist3r`, etc.).
   - If a required tool is missing, the command is incorrect.
4. **If the command is incorrect**, provide specific feedback:
   - Suggest the correct tools, flags, or arguments.
   - Provide an example correction.
5. **If the command is correct**, return an empty feedback string.

### Response Format:
- If incorrect: Explain the issue and provide the corrected command.
- If correct: Return an empty string.
"""


# LangChain prompt template
matcher_prompt = ChatPromptTemplate.from_messages(
    [
        ("system", system),
        ("human",
         "User question: {question}\nFeedback:\n{feedback_list}\nGenerated command:\n{generated_command}"),
    ]
)


# Chain
def get_syntax_checker(llm: ChatOpenAI):
    return matcher_prompt | llm.with_structured_output(SyntaxQuery)
