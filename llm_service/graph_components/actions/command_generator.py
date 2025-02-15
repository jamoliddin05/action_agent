from langchain import hub
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser

# Prompt
system = """You are an expert in generating Linux commands for the following tools: Sublist3r, Nmap, Kuro, and Impacket.
Your goal is to construct the most appropriate command based on the given user question and a list of feedback messages.
- Use feedback to refine the command structure.
- Ensure the command is syntactically correct and relevant to the tool mentioned.
- If multiple tools could be used, choose the most appropriate one based on context.
- Do not add extra explanations—output only the Linux command.
- No formatting is needed, just plain text linux command
"""

generator_prompt = ChatPromptTemplate.from_messages(
    [
        ("system", system),
        ("human", "User question: {question}\nFeedback:\n{feedback_list}"),
    ]
)

# Chain

def get_generator(llm: ChatOpenAI):
    return generator_prompt | llm | StrOutputParser()