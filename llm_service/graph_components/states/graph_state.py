from typing import List

from typing_extensions import TypedDict


class GraphState(TypedDict):
    """
    Represents the state of our graph.

    Attributes:
        question: question
        generated command: generated linux command
        feedbacks: list of feedbacks
    """

    input: str
    generated_command: str
    feedbacks: List[str]
    output: str
    command_matches_input: str
    output_matches_input: str
    response: str