from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser

# Prompt
system = """You are an expert at summarizing the execution results of Linux commands for the following tools: Sublist3r, Nmap, Kuro, and Impacket.
Your goal is to generate a structured, concise, and easy-to-understand summary based on:
1. The user’s original question.
2. The feedback messages used to refine the command.
3. The final generated Linux command.
4. The output produced by running the command.

### Summary Guidelines:
- Clearly state what the command was supposed to achieve.
- Summarize the key findings from the command output in a structured manner.
- If the command failed or produced an error, explain the issue briefly.
- Provide insights or potential next steps if relevant.
- Keep the summary short and clear, avoiding unnecessary technical jargon.
"""

summarizer_prompt = ChatPromptTemplate.from_messages(
    [
        ("system", system),
        (
            "human",
            "User question: {question}\n"
            "Feedback:\n{feedback_list}\n"
            "Generated command:\n{generated_command}\n"
            "Command output:\n{command_output}",
        ),
    ]
)

# Chain
def get_summarizer(llm: ChatOpenAI):
    return summarizer_prompt | llm | StrOutputParser()
