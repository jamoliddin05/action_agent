from dotenv import load_dotenv

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

llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)


def should_answer(state: GraphState) -> GraphState:
    print("Answer or not")
    user_input = state["input"]
    return get_question_router(llm).invoke({"question": user_input}).datasource


def generate_command(state: GraphState) -> GraphState:
    print("Generating command")
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
    print("Validating syntax")
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
    if state["command_matches_input"] == 'no':
        print("Regenerating")
        return "command_generator"

    return "execute"

def execute(state: GraphState) -> GraphState:
    print("Executing command")
    generated_command = state["generated_command"]
    response = execute_command(generated_command)

    return {
        "output": response.get("output"),
    }

def validate_output(state: GraphState) -> GraphState:
    print("Validating output")
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
    if state["output_matches_input"] == 'no':
        print("Regenerating")
        return "command_generator"
    return "wrapper"

def wrap_response(state: GraphState) -> GraphState:
    print("Wrap response")
    response = get_summarizer(llm).invoke({
        "question": state["input"],
        "feedback_list": state["feedbacks"],
        "generated_command": state["generated_command"],
        "command_output": state["output"],
    })

    return {"response": response}



