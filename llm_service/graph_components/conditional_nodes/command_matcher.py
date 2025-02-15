from typing import Literal
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from pydantic import BaseModel, Field


# Data model
class CommandQuery(BaseModel):
    """Determines if a generated command matches the user’s intent and execution feedback."""

    matches_user_input: Literal["yes", "no"] = Field(
        ...,
        description="Determine if the generated Linux command correctly follows the user's intent and past feedback.",
    )

    feedback: str = Field(
        description="Provide necessary corrections if the command is incorrect. If correct, return an empty string.",
    )


# Standard Command Syntax Reference
COMMAND_SYNTAX = {
    "Sublist3r": "sublist3r -d <domain> [-o <output_file>]",
    "Nmap": "nmap [-options] <target>",
}

# Convert syntax reference to formatted text
COMMAND_SYNTAX_TEXT = "\n".join(f"- **{tool}**: `{syntax}`" for tool, syntax in COMMAND_SYNTAX.items())

# System Prompt (Optimized)
system_prompt = f"""You are an expert in Linux security commands.
Your task is to verify that a given command:
- **Matches the user’s intent**.
- **Includes necessary tools and flags**.
- **Corrects mistakes based on previous feedback and execution output**.

### Steps:
1. **Analyze the user's question** to determine intent.
2. **Compare the command** to the correct syntax:
{COMMAND_SYNTAX_TEXT}
3. **Check command execution output**:
   - If errors suggest a missing flag or incorrect syntax, identify the issue.
   - If errors indicate a different tool is needed, suggest an alternative command.
4. **Provide specific corrections**:
   - If flags/arguments are wrong, specify the correct ones.
   - If additional context is needed, explain briefly.
5. **If correct**, return an empty feedback string.

### Response Format:
- **If incorrect**: Explain the issue and suggest the correct command.
- **If correct**: Return an empty string.
"""

# LangChain prompt template
matcher_prompt = ChatPromptTemplate.from_messages(
    [
        ("system", system_prompt),
        ("human",
         "User question: {question}\n"
         "Previous Feedback:\n{feedback_list}\n"
         "Generated Command:\n{generated_command}\n"
         "Command Execution Output:\n{command_output}"),
    ]
)


# Optimized chain function
def get_matcher(llm: ChatOpenAI):
    """Returns an LLM chain that validates and corrects generated Linux commands."""
    return matcher_prompt | llm.with_structured_output(CommandQuery)
