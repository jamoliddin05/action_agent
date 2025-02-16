from dotenv import load_dotenv
import requests
import sys
import aiohttp
import asyncio
import shutil

from langchain_openai import ChatOpenAI

from graph_components.states.graph_state import GraphState

from graph_components.conditional_nodes.question_router import get_question_router
from graph_components.conditional_nodes.command_matcher import get_matcher
from graph_components.conditional_nodes.syntax_checker import get_syntax_checker
from graph_components.actions.command_generator import get_generator
from graph_components.wrappers.summarizer import get_summarizer
from graph_components.conditional_nodes.question_router import get_question_router

from graph_components.actions.server_api import execute_command

load_dotenv()

# llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

from langchain_deepseek import ChatDeepSeek
llm = ChatDeepSeek(model='deepseek-chat', temperature=0)

def print_title(title: str):
    """Prints a single-line title centered within a full-width border."""
    terminal_width = shutil.get_terminal_size((80, 20)).columns  # Default width fallback: 80
    title = f" {title} "

    print(title.center(terminal_width, "-"))

def should_answer(state: GraphState) -> GraphState:
    print_title("ANSWER OR NOT")
    user_input = state["input"]
    return get_question_router(llm).invoke({"question": user_input}).datasource


def generate_command(state: GraphState) -> GraphState:
    print_title("GENERATING COMMAND")
    user_input = state["input"]
    feedbacks = state["feedbacks"]
    generated_command = get_generator(llm).invoke(
        {
            "question": user_input,
            "feedback_list": "\n".join(feedbacks)
        }
    )

    return {"generated_command": generated_command}


def validate_syntax(state: GraphState) -> GraphState:
    print_title("VALIDATING SYNTAX")
    validation = get_syntax_checker(llm).invoke({
        "question": state["input"],
        "feedback_list": state["feedbacks"],
        "generated_command": state["generated_command"],
    })

    return {
        "feedbacks": state["feedbacks"] + ([validation.feedback] if validation.feedback else []),
        "command_matches_input": validation.matches_user_input,
    }

def should_pass_validation(state: GraphState):
    print_title("SHOULD PASS SYNTAX VALIDATION")
    if state["command_matches_input"] == 'no':
        print("Regenerating")
        return "command_generator"

    return "execute"


def execute(state: GraphState) -> GraphState:
    print_title("EXECUTING COMMAND")
    generated_command = state["generated_command"]

    url = "http://mock_server:5000/execute"  # Replace with actual service URL

    collected_output = []

    with requests.post(url, json={"command": generated_command}, stream=True) as response:
        for line in response.iter_lines():
            if line:
                decoded_line = line.decode("utf-8")

                # Print output immediately for real-time updates
                print(decoded_line, flush=True)

                # Collect for returning full response
                collected_output.append(decoded_line)

    return {"output": "\n".join(collected_output)}

def validate_output(state: GraphState) -> GraphState:
    print_title("VALIDATING OUTPUT")
    validation = get_matcher(llm).invoke({
        "question": state["input"],
        "feedback_list": state["feedbacks"],
        "generated_command": state["generated_command"],
        "command_output": state["output"],
    })

    return {
        "feedbacks": state["feedbacks"] + ([validation.feedback] if validation.feedback else []),
        "output_matches_input": validation.matches_user_input,
    }

def should_pass_output_validation(state: GraphState):
    print_title("SHOULD PASS OUTPUT VALIDATION")
    if state["output_matches_input"] == 'no':
        print("Regenerating")
        return "command_generator"
    return "wrapper"

def wrap_response(state: GraphState) -> GraphState:
    print_title("WRAPPING RESPONSE")
    response = get_summarizer(llm).invoke({
        "question": state["input"],
        "feedback_list": state["feedbacks"],
        "generated_command": state["generated_command"],
        "command_output": state["output"],
    })

    return {"response": response}



