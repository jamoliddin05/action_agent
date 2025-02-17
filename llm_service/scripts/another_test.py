# from . import *
#
# from langchain_openai import ChatOpenAI
#
# from graph_components.conditional_nodes.question_router import get_question_router
# from graph_components.conditional_nodes.command_matcher import get_matcher
# from graph_components.actions.command_generator import get_generator
# from graph_components.wrappers.summarizer import get_summarizer
# from graph_components.conditional_nodes.question_router import get_question_router
#
# from .test import execute_command
#
# llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)
#
#
# query = "impacket google"
#
# forward_or_not = get_question_router(llm).invoke({"question": query})
#
# if forward_or_not.datasource == "command_generator":
#     generation = get_generator(llm).invoke({"question": query, "feedback_list": ""})
#
#     print(generation)
#
#     response = execute_command(generation)
#
#     is_matched = get_matcher(llm).invoke(
#         {
#             "question": query,
#             "feedback_list": "",
#             "generated_command": generation,
#             "command_output": response.get("output")
#         }
#     )
#
#     print(is_matched)
#
#     wrapper = get_summarizer(llm).invoke(
#         {
#             "question": query,
#             "feedback_list": "",
#             "generated_command": generation,
#             "command_output": response.get("output"),
#         }
#     )
#
#     print(wrapper)
# else:
#     print("It's not a cybersecurity related query")

from graph_components.conditional_nodes.user_feedback import get_user_checker
from graph_components.nodes import llm

response = get_user_checker(llm).invoke(
    {
        "feedback": "Everything is good",
        "generated_command": "nmap -p google.com"
    }
)

print(response)
